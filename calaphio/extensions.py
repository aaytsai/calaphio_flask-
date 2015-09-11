from flask import abort, render_template
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

# Flask-SQLAlchemy
from flask.ext.wtf import CsrfProtect

db = SQLAlchemy()

# Flask-Login
login_manager = LoginManager()

# Flask-WTF
csrf = CsrfProtect()

@csrf.error_handler
def csrf_error(reason):
    # TODO (ble) fill this method with custom view
    abort(400)