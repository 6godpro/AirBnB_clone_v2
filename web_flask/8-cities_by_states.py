#!/usr/bin/python3
"""
    Starts a Flask web application.

    Route: '/cities_by_states': Displays the list of states followed
           by their cities using HTML list.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    return render_template("8-cities_by_states.html",
                           all_states=storage.all(State).values())


@app.teardown_appcontext
def teardown_states_list(exception=None):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
