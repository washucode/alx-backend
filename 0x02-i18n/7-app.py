#!/usr/bin/env python3
"""
Force locale
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Union, Dict
import pytz

class Config:
    """
    Config class
    """
    DEBUG = True
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(id):
    """Get user"""
    return users.get(int(id), 0)


@babel.timezoneselector
def get_timezone() -> str:
    """
    Gets timezone from request object
    """
    tz = request.args.get('timezone', '').strip()
    if not tz and g.user:
        tz = g.user['timezone']
    try:
        return pytz.timezone(tz).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.before_request
def before_request() -> None:
    """Before request"""
    setattr(g, 'user', get_user(request.args.get('login_as', 0)))


@babel.localeselector
def get_locale() -> str:
    """Get locale"""

    options = [
        request.args.get('locale'),
        g.user['locale'],
        request.accept_languages.best_match(app.config['LANGUAGES']),
        app.config['BABEL_DEFAULT_LOCALE']
    ]
    for locale in options:
        if locale in app.config['LANGUAGES']:
            return locale

 
# babel = Babel(app, locale_selector=get_locale)


@app.route('/')
def index() -> str:
    """Return string"""
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run()
