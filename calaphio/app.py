from flask import Flask, Request
from flask_nav import register_renderer
from jinja2 import Markup
from scrubber import Scrubber
from werkzeug import url_decode;

from calaphio.core.models import User
from core import core
from extensions import db, login_manager, csrf, bootstrap, nav, BetterBootstrapRenderer

class MethodRewriteMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if 'METHOD_OVERRIDE' in environ.get('QUERY_STRING', ''):
            args = url_decode(environ['QUERY_STRING'])
            method = args.get('__METHOD_OVERRIDE__')
            if method:
                method = method.encode('ascii', 'replace')
                environ['REQUEST_METHOD'] = method
        return self.app(environ, start_response)

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

    # Method Rewriter
    app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)

    return app


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

