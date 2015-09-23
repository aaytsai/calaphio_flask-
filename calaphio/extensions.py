from dominate import tags
from flask import abort
from flask.ext.bootstrap import Bootstrap
from flask.ext.bootstrap.nav import BootstrapRenderer
from flask.ext.login import LoginManager, current_user
from flask.ext.nav import Nav
from flask.ext.nav.elements import Navbar, View, Link, NavigationItem
from flask.ext.sqlalchemy import SQLAlchemy

# Flask-SQLAlchemy
from flask.ext.wtf import CsrfProtect

db = SQLAlchemy()

# Flask-Login
login_manager = LoginManager()

# Flask-WTF
csrf = CsrfProtect()

# Flask-Bootstrap
bootstrap = Bootstrap()

# Flask-Nav
nav = Nav()


@csrf.error_handler
def csrf_error(reason):
    # TODO (ble) fill this method with custom view
    abort(400)


# Add Better RawTag because Flask-Nav sucks huge ^&$#
class Tag(NavigationItem):
    def __init__(self, tag, text, **attribs):
        self.tag = tag
        self.text = text
        self.attribs = attribs


class BetterBootstrapRenderer(BootstrapRenderer):
    def visit_Tag(self, node):
        item = tags.li()
        item.add(node.tag(node.text, **node.attribs))

        return item


@nav.navigation("navbar")
def navbar():
    if current_user.is_active():
        return Navbar(Link("Members@Calaphio", "/"),
                      Link("My Profile: " + current_user.fullname, "/"),
                      View("News", "core.NewsView:index"),
                      View("Logout", "core.UsersView:logout"))
    else:
        return Navbar(Link("Members@Calaphio", "/"),
                      View("News", "core.NewsView:index"),
                      Tag(tags.a, "Login", href="#", data_toggle="modal", data_target="#loginModal"))