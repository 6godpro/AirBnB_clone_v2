#!/usr/bin/python3
"""Creates and distributes an archive to the web servers."""

import os.path
from datetime import datetime
from fabric.api import (
    env,
    local,
    put,
    run
)

env.hosts = ['52.87.215.172', '100.26.231.127']
shared_file = None


def do_pack():
    """Creates a .tgz archive file."""
    dt = datetime.strftime(datetime.utcnow(), '%Y%m%d%H%M%S')
    file_path = "versions/web_static_{}.tgz".format(dt)
    if not os.path.exists('versions'):
        if local('mkdir -p versions').return_code != 0:
            return None
    command = "tar -cvzf {} web_static".format(file_path)
    if local(command).return_code != 0:
        return None
    return file_path


def do_deploy(archive_path):
    """Deploys an archive to the web servers."""
    if os.path.isfile(archive_path) is False:
        return False

    file = archive_path.split('/')[-1].split('.')[0]
    r_path = "/data/web_static/releases"

    if put(archive_path, '/tmp/{}.tgz'.format(file)).failed is True:
        return False

    if run('rm -rf {}/{}'.format(r_path, file)).failed is True:
        return False

    if run('mkdir -p {}/{}/'.format(r_path, file)).failed is True:
        return False

    if run('tar -xzf /tmp/{}.tgz -C {}/{}/'
           .format(file, r_path, file)).failed is True:
        return False

    if run('rm /tmp/{}.tgz'.format(file)).failed is True:
        return False

    command = "mv {}/{}/web_static/*".format(r_path, file)
    command += " {}/{}/".format(r_path, file)
    if run(command).failed is True:
        return False

    if run('rm -rf {}/{}/web_static'
           .format(r_path, file)).failed is True:
        return False

    if run('rm -rf /data/web_static/current').failed is True:
        return False

    if run('ln -s {}/{} /data/web_static/current'
           .format(r_path, file)).failed is True:
        return False
    return True


def deploy():
    """Creates and distributes an archive to web servers."""
    global shared_file
    deploy.flag = getattr(deploy, 'flag', False)
    if deploy.flag is False:
        shared_file = do_pack()
        deploy.flag = True
    if shared_file is None:
        return False

    return do_deploy(shared_file)


def do_clean(number=0):
    """Deletes out-of-date archives from the servers."""
    total_files = local('find versions/ -type f | wc -l', capture=True).stdout
    total_files = int(total_files) - int(number)
    if total_files >= 0:
        local('rm -f $(find versions -type f | head -n {})'.format(total_files))

    total_files = run('find /data/web_static/releases/'
                      ' -mindepth 1 -maxdepth 1 -type d | wc -l').stdout
    total_files = int(total_files) - int(number)
    if total_files >= 0:
        run('rm -rf $(find /data/web_static/releases/'
            ' -mindepth 1 -maxdepth 1 -type d -printf "%T@\t%p\n"'
            ' | sort -n | head -n {})'.format(total_files))
