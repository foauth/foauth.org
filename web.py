from functools import wraps
import os

from flask import request, redirect, render_template, abort
from flaskext.login import current_user, login_user, logout_user, login_required

import config
import forms
import models


@config.app.route('/')
def index():
    return render_template('index.html', login=forms.Login(), signup=forms.Signup())


@config.app.route('/about/')
def about():
    return render_template('about.html', login=forms.Login())


@config.app.route('/about/faq/')
def faq():
    return render_template('faq.html', login=forms.Login())


@config.app.route('/about/terms/')
def terms():
    return render_template('terms.html', login=forms.Login())


@config.app.route('/login/', methods=['POST'])
def login():
    form = forms.Login(request.form)
    if form.validate():
        user = models.User.query.filter_by(email=form.email.data).first()
        if not user:
            abort(404)
        if user.check_password(form.password.data):
            login_user(user)
            return redirect('/services/')
        return redirect('/')
    else:
        return render_template('index.html', login=form, signup=forms.Signup())


@config.app.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    return redirect('/')


@config.app.route('/signup/', methods=['POST'])
def signup():
    form = forms.Signup(request.form)
    if form.validate():
        user = models.User(email=form.email.data, password=form.password.data)
        models.db.session.add(user)
        models.db.session.commit()
        login_user(user)
        return redirect('/services/')
    else:
        return render_template('index.html', login=forms.Login(), signup=form)


@config.app.route('/services/', methods=['GET'])
def services():
    services = sorted((s.alias, s) for s in config.services)
    return render_template('services.html', login=forms.Login(), services=services)


def auth_endpoint(func):
    services = config.services
    @wraps(func)
    def wrapper(alias, *args, **kwargs):
        for service in services:
            if service.alias == alias:
                return func(service, *args, **kwargs)
        abort(404)
    return wrapper


@config.app.route('/services/<alias>/authorize', methods=['GET'])
@login_required
@auth_endpoint
def authorize(service):
    return service.authorize()


@config.app.route('/services/<alias>/callback', methods=['GET'])
@login_required
@auth_endpoint
def callback(service):
    key, secret = service.callback(request.args)
    user_key = models.Key.query.filter_by(user_id=current_user.id,
                                          service_alias=service.alias).first()
    if not user_key:
        user_key = models.Key(user_id=current_user.id,
                              service_alias=service.alias)
    user_key.key = key
    user_key.secret = secret
    models.db.session.add(user_key)
    models.db.session.commit()
    return redirect('/services/')


@config.app.route('/<domain>/<path:path>', methods=['GET', 'POST'])
@config.app.route('/<domain>/', defaults={'path': u''}, methods=['GET', 'POST'])
def api(domain, path):
    auth = request.authorization
    if auth:
        user = models.User.query.filter_by(email=auth.username).first()
        if user and user.check_password(auth.password):
            for service in config.services:
                for api_domain in service.api_domains:
                    if domain == api_domain:
                        key = user.keys.filter_by(service_alias=service.alias).first()
                        resp = service.api(key, domain, path)
                        content = resp.raw.read()
                        print 'CONTENT >>>>>>>>>>>>>>>>'
                        print type(content)
                        print len(content)
                        print content
                        return config.app.make_response((content,
                                                         resp.status_code,
                                                         resp.headers))
    abort(403)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    config.app.run(host='0.0.0.0', port=port, debug=True)
