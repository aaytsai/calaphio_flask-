from datetime import datetime

from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, url_for, redirect, render_template, abort, session, current_app, jsonify, request
from flask_classy import FlaskView, route
from flask_principal import identity_changed, AnonymousIdentity, Identity

from calaphio import db
from calaphio.core.forms import LoginForm, NewsitemForm
from calaphio.core.models import Newsitem, User, CalendarEvent
from calaphio.extensions import excomm_permission

core = Blueprint('core', __name__, template_folder='templates', static_folder="static", static_url_path='/static/core',
                 url_prefix='');


class NewsView(FlaskView):

    def index(self):
        news = db.session.query(Newsitem).order_by(Newsitem.created_at.desc()).all()

        return render_template('news/index.html', news=news)

    @login_required
    @excomm_permission.require(http_exception=403)
    def create(self):
        newsitem_form = NewsitemForm()
        return render_template('news/create.html', newsitem_form=newsitem_form)

    @login_required
    @excomm_permission.require(http_exception=403)
    def post(self):
        newsitem_form = NewsitemForm()
        newsitem = Newsitem()

        if newsitem_form.validate_on_submit():
            newsitem_form.populate_obj(newsitem)

            # Add user_id
            newsitem.user_id = current_user.user_id

            db.session.add(newsitem)
            db.session.commit()
            return redirect(url_for("core.NewsView:index"))

        return redirect(url_for("core.NewsView:create"))

    @login_required
    @excomm_permission.require(http_exception=403)
    def update(self, id):
        newsitem = Newsitem.query.get_or_404(id)
        newsitem_form = NewsitemForm(obj=newsitem)
        return render_template('news/update.html', newsitem_form=newsitem_form, id=id)

    @login_required
    @excomm_permission.require(http_exception=403)
    def put(self, id):
        newsitem = Newsitem.query.get_or_404(id)

        newsitem_form = NewsitemForm()
        if newsitem_form.validate_on_submit():
            newsitem_form.populate_obj(newsitem)

            db.session.add(newsitem)
            db.session.commit()
            return redirect(url_for("core.NewsView:index"))

        return redirect(url_for("core.NewsView:update", id))

    @login_required
    @excomm_permission.require(http_exception=403)
    def delete(self, id):
        newsitem = Newsitem.query.get_or_404(id)

        db.session.delete(newsitem)
        db.session.commit()
        return redirect(url_for("core.NewsView:index"))


class EventsView(FlaskView):

    @login_required
    def index(self):
        events = db.session.query(CalendarEvent).order_by(CalendarEvent.created_at.desc()).limit(100)

        return render_template('events/index.html', events=events)

    @login_required
    def get_events(self):
        ret = dict()

        begin = datetime.fromtimestamp(long(request.args.get('from')) / 1000.0)
        end = datetime.fromtimestamp(long(request.args.get('to')) / 1000.0)
        if begin is None or end is None:
            ret['success'] = 0
            ret['error'] = "Did not set 'to' and 'from' query parameters"
        else:
            # Need to show deleted events for admins though
            db_events = db.session.query(CalendarEvent)\
                .filter(CalendarEvent.start_at >= begin, CalendarEvent.end_at < end, CalendarEvent.deleted == False).all()
            events = []
            for db_event in db_events:
                event = dict()
                event['id'] = db_event.event_id
                event['title'] = db_event.title
                event['url'] = url_for("core.EventsView:partial_get", id=db_event.event_id)
                event['class'] = "event-" + db_event.event_type
                event['start'] = long(db_event.start_at.strftime("%s")) * 1000
                event['end'] = long(db_event.end_at.strftime("%s")) * 1000

                events.append(event)

            ret['success'] = 1
            ret['result'] = events

        return jsonify(**ret)

    def partial_get(self, id):
        event = CalendarEvent.query.options(db.joinedload_all('event_attends.attendee'),
                                            db.joinedload_all('comments.poster')).get_or_404(id)

        return render_template('events/partial_get.html', event=event)

class UsersView(FlaskView):
    @route('/login', methods=["POST"])
    def login(self):
        login_form = LoginForm()
        if login_form.validate_on_submit():
            user, authenticated = User.authenticate(login_form.email.data, login_form.password.data)

            if authenticated:
                login_user(user, remember=login_form.remember_me.data)

                # Tell Flask-Principal the identity changed
                identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.user_id))

        return redirect(url_for("core.NewsView:index"))

    @login_required
    def logout(self):
        logout_user()

        # Remove session keys set by Flask-Principal
        for key in ('identity.name', 'identity.auth_type'):
            session.pop(key, None)

        # Tell Flask-Principal the user is anonymous
        identity_changed.send(current_app._get_current_object(),
                              identity=AnonymousIdentity())

        return redirect(url_for("core.NewsView:index"))


NewsView.register(core)
EventsView.register(core)
UsersView.register(core)

# Home page is just the main news page for now
@core.route('/')
def home_page():
    return redirect(url_for("core.NewsView:index"))


@core.context_processor
def inject_globals():
    return dict(login_form=LoginForm())
