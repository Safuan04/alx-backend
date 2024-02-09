#!/usr/bin/env python3
""" Get locale from request
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime
from pytz import timezone, UnknownTimeZoneError
from datetime import datetime


app = Flask(__name__)
babel = Babel(app)


@babel.timezoneselector
def get_timezone():
    """gets match timezone"""
    timezone_url = request.args.get('timezone')
    if timezone_url:
        try:
            timezone(timezone_url)
            return timezone(timezone_url)
        except UnknownTimeZoneError:
            print(f'timezone doesnt exist: {timezone_url}')

    if hasattr(g, 'user') and g.user:
        users_timezone = g.user.get('timezone')
        if users_timezone:
            try:
                timezone(users_timezone)
                return timezone(users_timezone)
            except UnknownTimeZoneError:
                print(f"timezone doesnt exist: {users_timezone}")

    default_timezone = Config.BABEL_DEFAULT_TIMEZONE
    return timezone(default_timezone)


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

    if hasattr(g, 'user') and g.user:
        user_lang = g.user.get('local')
        if user_lang and user_lang in Config.LANGUAGES:
            return user_lang

    best_match = request.accept_languages.best_match(Config.LANGUAGES)
    if best_match:
        return best_match

    return Config.BABEL_DEFAULT_LOCALE


@app.route("/")
def welcome():
    """ Simply outputs “Welcome to Holberton” as page title (<title>)
    -   and “Hello world” as header (<h1>)
    """
    username = None
    timezone = get_timezone()
    current_time = datetime.now(timezone)
    print(current_time)
    updated_time = format_datetime(current_time)
    print(updated_time)
    if hasattr(g, 'user') and g.user:
        username = g.user.get('name')
    return render_template('index.html', username=username,
                           timezone=updated_time)


if __name__ == '__main__':
    app.run(debug=True)
