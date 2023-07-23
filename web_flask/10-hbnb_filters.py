#!/usr/bin/python3
"""
    Starts a Flask web application.

    Route: '/hbnb_filters': HBNB filters.
"""

from flask import Flask, render_template
from models import storage
from models.amenity import Amenity
from models.state import State

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    return render_template("10-hbnb_filters.html",
                           all_states=storage.all(State).values(),
                           amenities=storage.all(Amenity).values())


@app.teardown_appcontext
def teardown_states_list(exception=None):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
