from flask.ext.login import login_user, current_user, login_required, logout_user
from calaphio import db

from flask import abort, Blueprint, url_for, redirect, render_template
from flask.ext.classy import FlaskView, route
from calaphio.core.forms import LoginForm
from calaphio.core.models import Newsitem, User

core = Blueprint('core', __name__, template_folder='templates', url_prefix='');

class NewsView(FlaskView):

    def index(self):
        news = db.session.query(Newsitem).all()
        login_form = LoginForm()

        return render_template('news/index.html', news=news, login_form=login_form)

class UsersView(FlaskView):

    @route('/login', methods=["POST"])
    def login(self):
        login_form = LoginForm()
        if login_form.validate_on_submit():
            user, authenticated = User.authenticate(login_form.email.data, login_form.password.data)

            if authenticated:
                login_user(user, remember=login_form.remember_me.data)

        return redirect(url_for("core.NewsView:index"))

    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for("core.NewsView:index"))


NewsView.register(core)
UsersView.register(core)

# Home page is just the main news page for now
@core.route('/')
def home_page():
    return redirect(url_for("core.NewsView:index"))