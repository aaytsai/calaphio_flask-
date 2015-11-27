import datetime
import hashlib

from flask_login import UserMixin, current_user
from sqlalchemy import orm, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref

from calaphio import db, TimestampMixin
from calaphio.extensions import admin_permission, active_permission, pledge_permission

class EventType(object):
    SERVICE = "service"
    FELLOWSHIP = "fellowship"
    FUNDRAISER = "fundraiser"
    RUSH = "rush"
    ALUMNI = "alumni"
    INTERCHAPTER = "interchapter"
    LEADERSHIP = "leadership"
    UNKNOWN = "unknown"

class Newsitem(TimestampMixin, db.Model):
    __tablename__ = "newsitems"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('apo_users.user_id'), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    pledge = db.Column(db.Boolean, nullable=False)
    everyone = db.Column(db.Boolean, nullable=False)

    @property
    def can_be_viewed_by_current_user(self):
        return self.everyone or \
               admin_permission.can() or \
               (self.active and active_permission.can()) or \
               (self.pledge and pledge_permission.can())


class ActiveMember(db.Model):
    __tablename__ = "apo_actives"

    user_id = db.Column(db.Integer, ForeignKey('apo_users.user_id'), primary_key=True)


class PledgeMember(db.Model):
    __tablename__ = "apo_pledges"

    user_id = db.Column(db.Integer, ForeignKey('apo_users.user_id'), primary_key=True)

user_roles = db.Table('apo_permissions_groups',
    db.Column('group_id', db.Integer, ForeignKey('apo_permissions_groups_control.group_id')),
    db.Column('user_id', db.Integer, ForeignKey('apo_users.user_id'))
)

class User(UserMixin, db.Model):
    __tablename__ = "apo_users"

    user_id = db.Column(db.Integer, primary_key=True)

    # Login Info
    email = db.Column(db.String(255), nullable=False)
    passphrase = db.Column(db.String(40), nullable=False)
    salt = db.Column(db.String(32), nullable=False)

    # User Info
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    pledgeclass = db.Column(db.String(255), nullable=False)
    cellphone = db.Column(db.String(255), nullable=False)

    # Fields used to determine if active
    disabled = db.Column(db.Boolean, nullable=False)
    depledged = db.Column(db.Boolean, nullable=False)

    # Relationships <3
    active_member = relationship(ActiveMember, uselist=False, backref="user")
    pledge_member = relationship(PledgeMember, uselist=False, backref="user")
    posts = relationship('Newsitem', backref="poster")
    roles = relationship("Role", secondary=user_roles, backref="users")

    @classmethod
    def authenticate(cls, email, password):
        user = db.session.query(User).filter(User.email == email).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    def check_password(self, password):
        return hashlib.sha1(self.salt + password).hexdigest() == self.passphrase

    def is_active(self):
        return (not self.disabled) and (not self.depledged)

    def get_id(self):
        return unicode(self.user_id)

    @property
    def fullname(self):
        return self.firstname + " " + self.lastname


class Role(db.Model):
    __tablename__ = "apo_permissions_groups_control"

    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class CalendarEvent(TimestampMixin, db.Model):
    __tablename__ = "apo_calendar_event"

    # Event Metadata
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    start_at = db.Column(db.DateTime, nullable=True)
    end_at = db.Column(db.DateTime, nullable=True)
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    #Event Types
    type_service_chapter = db.Column(db.Boolean, nullable=False, default=False)
    type_service_campus = db.Column(db.Boolean, nullable=False, default=False)
    type_service_community = db.Column(db.Boolean, nullable=False, default=False)
    type_service_country = db.Column(db.Boolean, nullable=False, default=False)

    type_fellowship = db.Column(db.Boolean, nullable=False, default=False)
    type_interchapter = db.Column(db.Boolean, nullable=False, default=False)
    type_fundraiser = db.Column(db.Boolean, nullable=False, default=False)
    type_rush = db.Column(db.Boolean, nullable=False, default=False)
    type_alumni = db.Column(db.Boolean, nullable=False, default=False)
    type_leadership = db.Column(db.Boolean, nullable=False, default=False)

    type_active_meeting = db.Column(db.Boolean, nullable=False, default=False)
    type_pledge_meeting = db.Column(db.Boolean, nullable=False, default=False)

    # Signup Logic
    signup_begin = db.Column(db.Date, nullable=True)
    signup_cutoff = db.Column(db.Date, nullable=True)
    signup_limit = db.Column(db.Integer, nullable=False, default=0)

    # Relationships <3

    @property
    def chair_attends(self):
        return [event_attend for event_attend in self.event_attends if event_attend.chair]

    @property
    def attends(self):
        if self.signup_limit > 0:
            return self.event_attends[:self.signup_limit]
        else:
            return self.event_attends

    @property
    def waitlist(self):
        if self.signup_limit > 0:
            return self.event_attends[self.signup_limit:]
        else:
            return None

    @property
    def event_type(self):
        if self.type_service_chapter or self.type_service_campus or \
                self.type_service_community or self.type_service_country:
            return EventType.SERVICE
        elif self.type_fellowship:
            return EventType.FELLOWSHIP
        elif self.type_fundraiser:
            return EventType.FUNDRAISER
        elif self.type_rush:
            return EventType.RUSH
        elif self.type_alumni:
            return EventType.ALUMNI
        elif self.type_interchapter:
            return EventType.INTERCHAPTER
        elif self.type_leadership:
            return EventType.LEADERSHIP
        else:
            return EventType.UNKNOWN



class CalendarAttend(db.Model):
    __tablename__ = "apo_calendar_attend"

    event_id = db.Column(db.Integer, ForeignKey('apo_calendar_event.event_id'), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('apo_users.user_id'), primary_key=True)
    chair = db.Column(db.Boolean, nullable=False, default=False)
    signup_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    event = relationship('CalendarEvent', backref=backref("event_attends", order_by="CalendarAttend.signup_time"))
    attendee = relationship('User')


class CalendarComment(db.Model):
    __tablename__ = "apo_calendar_comment"

    comment_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, ForeignKey('apo_calendar_event.event_id'), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('apo_users.user_id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    body = db.Column(db.Text, nullable=False)
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    event = relationship('CalendarEvent', backref=backref("comments", order_by="CalendarComment.timestamp"))
    poster = relationship('User')


