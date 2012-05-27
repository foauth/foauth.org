from flask.ext.wtf import Form, TextField, PasswordField, BooleanField, validators

import models


class Signup(Form):
    email = TextField('Email', [
        validators.Required('It&rsquo;s okay, we won&rsquo;t email you unless you want us to.'),
        validators.Email('Um, that doesn&rsquo;t look like an email address.'),
    ])
    password = PasswordField('Password', [
        validators.Required('How else will we know it&rsquo;s really you?'),
        validators.EqualTo('retype', message='If you can&rsquo;t type it twice now, you&rsquo;ll never be able to login with it.')
    ])
    retype = PasswordField('(again)')
    consent = BooleanField('Accept the Terms', [
        validators.Required('Don&rsquo;t worry, they&rsquo;re really simple.')
    ])

    def validate_email(form, field):
        if models.User.query.filter_by(email=field.data).count():
            raise validators.ValidationError('Looks like you&rsquo;ve already registered. Try the login box at the top.')


class Login(Form):
    email = TextField('Email', validators=[
        validators.Email('Please supply an email address.')
    ])
    password = PasswordField('Password', validators=[
        validators.Required('Please supply a password.')
    ])


