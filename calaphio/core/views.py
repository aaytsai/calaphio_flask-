from calaphio import db

from flask import Blueprint, url_for, redirect, render_template
from flask.ext.classy import FlaskView
from calaphio.core.models import Newsitem

core = Blueprint('core', __name__, template_folder='templates', url_prefix='');

class NewsView(FlaskView):

    def index(self):
        news = db.session.query(Newsitem).all()
        return render_template('news/index.html', news=news)

NewsView.register(core)

# Home page is just the main news page for now
@core.route('/')
def home_page():
    return redirect(url_for("core.NewsView:index"))