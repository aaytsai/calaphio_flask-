import hashlib

from flask.ext.login import UserMixin

from calaphio import db, TimestampMixin


class Newsitem(TimestampMixin, db.Model):
    __tablename__ = "newsitems"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    pledge = db.Column(db.Boolean, nullable=False)
    everyone = db.Column(db.Boolean, nullable=False)


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






