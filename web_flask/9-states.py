#!/usr/bin/python3
"""
    Starts a Flask web application.

    Route: '/states': Displays the list of states.
           '/states/<id>': Displays state followed by the cities
           in them if <id> is a valid state id, otherwise it
           displays 'Not found!'.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states/<id>", strict_slashes=False)
@app.route("/states", strict_slashes=False)
def states(id=None):
    if id is not None:
        state = [state for state in storage.all(State).values()
                 if id == state.id]
        if len(state) < 1:
            return render_template("9-states.html", valid='false')
        return render_template("9-states.html", state=state[0], valid='true')
    return render_template("9-states.html",
                           all_states=storage.all(State).values())


@app.teardown_appcontext
def teardown_states_list(exception=None):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
