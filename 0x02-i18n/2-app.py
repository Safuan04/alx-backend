#!/usr/bin/env python3
"""Get locale from request"""
from flask import Flask, render_template, request
from flask_babel import Babel


app = Flask(__name__)


class Config():
    """ class that has a LANGUAGES class attribute
    -   equal to ["en", "fr"]
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


def get_locale():
    """ determine the best match with our supported languages
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/")
def welcome():
    """ simply outputs “Welcome to Holberton” as page title (<title>)
    -   and “Hello world” as header (<h1>)"""
    return render_template('2-index.html')


babel = Babel(app, locale_selector=get_locale)
app.config.from_object(Config)
if __name__ == '__main__':
    app.run()
