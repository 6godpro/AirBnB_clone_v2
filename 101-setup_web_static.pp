# Sets up a server for deployment of a static website.
# update machine
exec { 'Update':
  provider => shell,
  command  => 'apt update -y',
}
-> package { 'nginx':
  ensure   => present,
  provider => 'apt',
}

-> exec { '/data/web_static/releases/test':
  command  => 'sh -c "mkdir -p /data/web_static/releases/test"',
  provider => shell,
}

-> exec { 'shared':
  command  => 'sh -c "mkdir -p /data/web_static/shared"',
  provider => shell,
}

-> file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => "My Static Page\n",
}

-> file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
}

-> exec { 'chown -R ubuntu:ubuntu /data':
  provider => shell,
}

-> file { '/var/www/html/index.html':
  ensure  => present,
  content => "Hello World!\n",
}

-> exec { 'server block config':
  provider => shell,
  command  => 'printf %s "server {
       listen 80 default_server;
       listen [::]:80 default_server;

       add_header X-Served-By $HOSTNAME;

       root /var/www/html;
       index index.html index.htm;

       location /redirect_me {
       		     return 301 https://www.google.com;
       }

       location / {
             try_files \$uri \$uri/ =404;
       }

       location /hbnb_static {
       		     alias /data/web_static/current;
             try_files \$uri \$uri/ =404;
       }

       error_page 404 /error404.html;
       # disable error404.html page for external access
       location = /error404.html {
              root /var/www/html;
      	            internal;
       }
}" > /etc/nginx/sites-available/default',
}

-> exec { 'restart':
  command => '/etc/init.d/nginx restart',
}
