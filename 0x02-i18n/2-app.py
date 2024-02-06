#!/usr/bin/env python3
""" Get locale from request
"""
from flask import Flask, render_template, request
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


class Config:
    """ Configuration class
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


@babel.localeselector
def get_locale() -> str:
    """ Determine the best match with our supported languages
    """
    return request.accept_languages.best_match(Config.LANGUAGES)


app.config.from_object(Config)


@app.route("/")
def welcome():
    """ Simply outputs “Welcome to Holberton” as page title (<title>)
    -   and “Hello world” as header (<h1>)
    """
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run(debug=True)
