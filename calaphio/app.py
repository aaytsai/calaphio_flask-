from flask import Flask
from jinja2 import Markup
from scrubber import Scrubber

from core import core
from extensions import db

scrubber = Scrubber()

# Jinja filter!
def sanitize_html(text):
    return Markup(scrubber.scrub(text))

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('CALAPHIO_CONFIG')

    #Register Blueprints
    app.register_blueprint(core)

    #Register Jinja Filters
    app.jinja_env.filters['sanitize_html'] = sanitize_html

    #Extensions
    db.init_app(app)

    return app

