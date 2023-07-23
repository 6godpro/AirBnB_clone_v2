#!/usr/bin/python3
"""
    Starts a Flask web application.

    Route: '/states_list': Displays the list of states using HTML list.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    return render_template("7-states_list.html",
                           all_states=storage.all(State).values())


@app.teardown_appcontext
def teardown_states_list(exception=None):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
