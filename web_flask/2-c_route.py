#!/usr/bin/python3
"""
    Starts a Flask web application.

    Routes:
        /         : Displays 'Hello HBNB!'
        /hbnb     : Displays 'HBNB'
        /c/<text> : Displays 'C <text>'
"""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """ Displays 'Hello HBNB!' """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ Displays 'HBNB' """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_hbnb(text):
    """
       Displays 'C followed by value of <text>'
    """
    text = text.replace('_', ' ')
    return f"C {escape(text)}"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
