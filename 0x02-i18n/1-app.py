#!/usr/bin/env python3
from flask import Flask, render_template
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)

class Config():
    """ class that has a LANGUAGES class attribute
    -   equal to ["en", "fr"]
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@app.route("/")
def welcome():
    """ simply outputs “Welcome to Holberton” as page title (<title>)
    -   and “Hello world” as header (<h1>)"""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run()
