from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import login

from config import app
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email = email
        self.password = self.hash_password(password)

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

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
    service_alias = db.Column(db.String(255))
    key = db.Column(db.String(255))
    secret = db.Column(db.String(255))

    user = db.relationship('User', backref=db.backref('keys', lazy='dynamic'))

    @property
    def service(self):
        if self.service_alias:
            for service in config.services:
                if self.service_alias == service.alias:
                    return service
        else:
            raise AttributeError('No service specified.')
        raise AttributeError('%r is not a valid service.' % self.service_alias)


login_manager = login.LoginManager()
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


