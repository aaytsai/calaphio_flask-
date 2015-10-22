from dominate import tags
from flask import abort
from flask_bootstrap import Bootstrap
from flask_bootstrap.nav import BootstrapRenderer
from flask_login import LoginManager, current_user
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Link, NavigationItem
from flask_sqlalchemy import SQLAlchemy

# Flask-SQLAlchemy
from flask_wtf import CsrfProtect

db = SQLAlchemy()

# Flask-Login
login_manager = LoginManager()
login_manager.login_view = "core.NewsView:index"
login_manager.login_message = "Please Login Before Performing That Action"

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
        if current_user.is_admin:
            return Navbar(Link("Members@Calaphio", "/"),
                          Link("My Profile: " + current_user.fullname, "/"),
                          View("News", "core.NewsView:index"),
                          View("Post News", "core.NewsView:create"),
                          View("Logout", "core.UsersView:logout"))
        else:
            return Navbar(Link("Members@Calaphio", "/"),
                          Link("My Profile: " + current_user.fullname, "/"),
                          View("News", "core.NewsView:index"),
                          View("Logout", "core.UsersView:logout"))
    else:
        return Navbar(Link("Members@Calaphio", "/"),
                      View("News", "core.NewsView:index"),
                      Tag(tags.a, "Login", href="#", data_toggle="modal", data_target="#loginModal"))
