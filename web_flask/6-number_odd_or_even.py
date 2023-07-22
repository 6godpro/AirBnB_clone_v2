#!/usr/bin/python3
"""
    Starts a Flask web application.

    Routes:
      /                       : Displays 'Hello HBNB!'
      /hbnb                   : Displays 'HBNB'
      /c/<text>               : Displays 'C <text>'
      /python/<text>          : if a <text> was provided Displays 'Python <text>'
                                Otherwise, it displays 'Python is cool'
      /number/<n>             : Displays '<n> is a number' only if n is an
                                integer.
      /number_template/<n>    : Display a HTML page only if n is an integer
      /number_odd_or_even/<n> : Display a HTML page only if n is an integer
                                Displays 'Number: <n> is even' if n is even.
                                Displays 'Number: <n> is odd' if n is odd.
"""
from flask import Flask, render_template
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
def c(text):
    """
       Displays 'C followed by value of <text>'
    """
    text = text.replace('_', ' ')
    return f"C {escape(text)}"


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text="is_cool"):
    """
       Displays 'Python followed by value of <text>'
    """
    text = text.replace('_', ' ')
    return f"Python {escape(text)}"


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """ Displays '<n> is a number' """
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """ Displays 'Number: <n>' """
    return render_template("5-number.html", number=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """ Displays 'Number: <n> is odd|even' """
    return render_template("6-number_odd_or_even.html", number=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
