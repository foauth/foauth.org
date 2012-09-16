from flask.ext.wtf import Form, TextField, PasswordField, BooleanField, validators

import models


class Signup(Form):
    email = TextField('Email address', [
        validators.Required('It&rsquo;s okay, we won&rsquo;t email you unless you want us to.'),
        validators.Email('Um, that doesn&rsquo;t look like an email address.'),
    ])
    password = PasswordField('Password', [
        validators.Required('How else will we know it&rsquo;s really you?'),
        validators.EqualTo('retype', message='If you can&rsquo;t type it twice now, you&rsquo;ll never be able to log in with it.')
    ])
    retype = PasswordField('Password (again)')
    consent = BooleanField('Accept the Terms', [
        validators.Required('Is there something you don&rsquo;t agree with?')
    ])

    def validate_email(form, field):
        if models.User.query.filter_by(email=field.data).count():
            raise validators.ValidationError('Looks like you&rsquo;ve already registered. Try the login box at the top.')


class Login(Form):
    email = TextField('Email address', validators=[
        validators.Email('Please supply an email address.')
    ])
    password = PasswordField('Password', validators=[
        validators.Required('Please supply a password.')
    ])


