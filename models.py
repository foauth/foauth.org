import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import login

import config
db = SQLAlchemy(config.app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = self.hash_password(password)

    def is_authenticated(self):
        return self.id is not None

    def is_anonymous(self):
        return False

    def is_active(self):
        return self.is_authenticated()

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User: %s>' % self.email

    def key_for_service(self, alias):
        return self.keys.filter_by(service_alias=alias).first()


class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_alias = db.Column(db.String)
    access_token = db.Column(db.String)
    secret = db.Column(db.String)
    expires = db.Column(db.DateTime)
    refresh_token = db.Column(db.String)
    service_user_id = db.Column(db.String)

    user = db.relationship('User', backref=db.backref('keys', lazy='dynamic'))

    @property
    def service(self):
        if not self.service_alias:
            raise AttributeError('No service specified.')
        try:
            return config.alias_map[self.service_alias]
        except KeyError:
            raise AttributeError('%r is not a valid service.' % self.service_alias)

    def update(self, data):
        self.access_token = data['access_token']
        self.secret = data.get('secret', None)
        if data.get('expires_in'):
            # Convert to a real datetime
            expires_in = datetime.timedelta(seconds=int(data['expires_in']))
            self.expires = datetime.datetime.now() + expires_in
        else:
            self.expires = None
        self.refresh_token = data.get('refresh_token', None)

    def is_expired(self):
        return self.will_expire(days=0)

    def will_expire(self, days=7):
        soon = datetime.datetime.now() + datetime.timedelta(days=days)
        return self.expires and self.expires < soon

    def fill_user_id(self):
        try:
            self.service_user_id = self.service.get_user_id(self)
        except Exception:
            # Normally `except Exception` would be a tremendously terrible
            # idea, but in this case a lot of things can go wrong, and the
            # end result is simply that the key couldn't be retrieved. In
            # that case, we can still handle it gracefully and return None.
            self.service_user_id = None


login_manager = login.LoginManager()
login_manager.setup_app(config.app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
