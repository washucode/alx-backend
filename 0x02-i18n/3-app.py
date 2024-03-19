#!/usr/bin/env python3
"""
Support languages
"""

from flask import Flask, render_template, request
from flask_babel import Babel


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


@babel.localeselector
def get_locale():
    """Get locale"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


# babel = Babel(app, locale_selector=get_locale)


@app.route('/')
def index():
    """Return string"""
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run()
