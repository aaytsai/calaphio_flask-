from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, url_for, redirect, render_template
from flask_classy import FlaskView, route

from calaphio import db
from calaphio.core.forms import LoginForm, NewsitemForm
from calaphio.core.models import Newsitem, User

core = Blueprint('core', __name__, template_folder='templates', static_folder="static", static_url_path='/static/core',
                 url_prefix='');


class NewsView(FlaskView):
    def index(self):
        news = db.session.query(Newsitem).order_by(Newsitem.created_at.desc()).all()
        login_form = LoginForm()

        return render_template('news/index.html', news=news)

    def create(self):
        newsitem_form = NewsitemForm()

        return render_template('news/create.html', newsitem_form=newsitem_form);

    def post(self):
        newsitem_form = NewsitemForm()
        if current_user.is_active() and current_user.is_admin and newsitem_form.validate_on_submit():
            newsitem = Newsitem()
            newsitem_form.populate_obj(newsitem)

            # Add user_id
            newsitem.user_id = current_user.user_id

            db.session.add(newsitem)
            db.session.commit()

        return redirect(url_for("core.NewsView:index"))

    def put(self):
        pass

    def delete(self):
        pass


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


@core.context_processor
def inject_globals():
    return dict(login_form=LoginForm())
