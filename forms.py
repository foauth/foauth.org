from flask.ext.wtf import Form, TextField, PasswordField, BooleanField, validators

import models


class Signup(Form):
    email = TextField('Email address', [
        validators.Required('It\'s okay, we won\'t email you unless you want us to.'),
        validators.Email('Um, that doesn\'t look like an email address.'),
    ])
    password = PasswordField('Password', [
        validators.Required('How else will we know it\'s really you?'),
        validators.EqualTo('retype', message='If you can't type it twice now, you'll never be able to log in with it.')
    ])
    retype = PasswordField('Password (again)')
    consent = BooleanField('Accept the Terms', [
        validators.Required('Is there something you don\'t agree with?')
    ])

    def validate_email(form, field):
        if models.User.query.filter_by(email=field.data).count():
            raise validators.ValidationError('Looks like you\'ve already registered. Try logging in instead.')


class Login(Form):
    email = TextField('Email address', validators=[
        validators.Email('Please supply an email address.')
    ])
    password = PasswordField('Password', validators=[
        validators.Required('Please supply a password.')
    ])


class Password(Form):
    password = PasswordField('Password', [
        validators.Required('How else will we know it\'s really you?'),
    ])
    retype = PasswordField('Password (again)', [
        validators.EqualTo('password', message='If you can't type it twice now, you'll never be able to log in with it.')
    ])
