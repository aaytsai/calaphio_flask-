import hashlib

from flask_login import UserMixin, current_user
from sqlalchemy import orm, ForeignKey
from sqlalchemy.orm import relationship

from calaphio import db, TimestampMixin
from calaphio.extensions import admin_permission, active_permission, pledge_permission


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

    # Fields used to determine if active
    disabled = db.Column(db.Boolean, nullable=False)
    depledged = db.Column(db.Boolean, nullable=False)

    # Relationships <3
    active_member = relationship(ActiveMember, uselist=False, backref="user")
    pledge_member = relationship(PledgeMember, uselist=False, backref="user")
    posts = relationship(Newsitem, backref="poster")
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

    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)





