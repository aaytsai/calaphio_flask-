import datetime

from extensions import db


"""
Mixin to allow for automatic created at/updated at timestamps for db records
"""


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)