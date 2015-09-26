from flask import Flask
from flask_nav import register_renderer
from jinja2 import Markup
from scrubber import Scrubber

from calaphio.core.models import User
from core import core
from extensions import db, login_manager, csrf, bootstrap, nav, BetterBootstrapRenderer


scrubber = Scrubber()

# Jinja filter!
def sanitize_html(text):
    return Markup(scrubber.scrub(text))


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('CALAPHIO_CONFIG')

    # Register Blueprints
    app.register_blueprint(core)

    # Register Jinja Filters
    app.jinja_env.filters['sanitize_html'] = sanitize_html

    # Extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    bootstrap.init_app(app)
    nav.init_app(app)
    register_renderer(app, "renderer", BetterBootstrapRenderer)

    return app


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

