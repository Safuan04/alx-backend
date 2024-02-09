#!/usr/bin/env python3
""" Get locale from request
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """ returns a user dictionary or None if the ID cannot be found
    -   or if login_as was not passed
    """
    user_request = request.args.get('login_as')
    if user_request:
        user = users.get(int(user_request))
        if user:
            return user
    return None


@app.before_request
def before_request():
    """ sets globally the user if found
    """
    user = get_user()
    if user:
        print(user)
        g.user = user


class Config:
    """ Configuration class
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale() -> str:
    """ Determine the best match lang with our supported languages
    """
    locale = request.args.get('locale')
    if locale and locale in Config.LANGUAGES:
        return locale
    return request.accept_languages.best_match(Config.LANGUAGES)


@app.route("/")
def welcome():
    """ Simply outputs “Welcome to Holberton” as page title (<title>)
    -   and “Hello world” as header (<h1>)
    """
    username = None
    if hasattr(g, 'user') and g.user:
        username = g.user.get('name')
    return render_template('5-index.html', username=username)


if __name__ == '__main__':
    app.run(debug=True)
