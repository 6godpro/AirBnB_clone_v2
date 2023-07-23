#!/usr/bin/python3
"""
    Starts a Flask web application.

    Route: '/states_list': Displays the list of states using HTML list.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    # for state in (storage.all(State).values()):
    #     print(dir(state))
    return render_template("8-cities_by_states.html",
                           all_states=storage.all(State).values())


@app.teardown_appcontext
def teardown_states_list(exception=None):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
