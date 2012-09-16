from functools import wraps
import os

from flask import request, flash, redirect, render_template, abort, url_for, make_response
from flask.ext.login import current_user, login_user, logout_user, login_required

from foauth import OAuthDenied, OAuthError
import config
import forms
import models


@config.app.errorhandler(403)
def forbidden(e):
    return make_response(render_template('403.html'), 403)


@config.app.route('/', methods=['GET'])
def index():
    return render_template('index.html', form=forms.Signup())


@config.app.route('/about/', methods=['GET'])
def about():
    return render_template('about.html')


@config.app.route('/about/faq/', methods=['GET'])
def faq():
    return render_template('faq.html')


@config.app.route('/about/terms/', methods=['GET'])
def terms():
    return render_template('terms.html')


@config.app.route('/login/', methods=['GET'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('services'))

    return render_template('login.html', form=forms.Login())


@config.app.route('/login/', methods=['POST'])
def login_post():
    form = forms.Login(request.form)
    if form.validate():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('services'))
        else:
            flash('Incorrect login', 'error')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', form=form)


@config.app.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@config.app.route('/signup/', methods=['POST'])
def signup():
    form = forms.Signup(request.form)
    if form.validate():
        user = models.User(email=form.email.data, password=form.password.data)
        models.db.session.add(user)
        models.db.session.commit()
        login_user(user)
        return redirect(url_for('services'))
    else:
        return render_template('index.html', form=form)


@config.app.route('/password/', methods=['GET'])
def password():
    return render_template('password.html', form=forms.Password())


@config.app.route('/password/', methods=['POST'])
@login_required
def password_post():
    form = forms.Password(request.form)
    if form.validate():
        current_user.set_password(form.data['password'])
        models.db.session.add(current_user)
        models.db.session.commit()
        return redirect(url_for('services'))
    else:
        return render_template('password.html', form=form)


@config.app.route('/services/', methods=['GET'])
def services():
    services = sorted((s.alias, s) for s in config.services)
    return render_template('services.html', services=services)


def auth_endpoint(func):
    @wraps(func)
    def wrapper(alias, *args, **kwargs):
        try:
            service = config.alias_map[alias]
        except KeyError:
            abort(404)
        return func(service, *args, **kwargs)
    return wrapper


@config.app.route('/services/<alias>/authorize', methods=['GET'])
@login_required
@auth_endpoint
def authorize(service):
    try:
        return service.authorize()
    except OAuthError:
        flash('Error occured while authorizing %s' % service.name, 'error')
        return redirect(url_for('services'))


@config.app.route('/services/<alias>/callback', methods=['GET'])
@login_required
@auth_endpoint
def callback(service):
    user_key = models.Key.query.filter_by(user_id=current_user.id,
                                          service_alias=service.alias).first()
    try:
        data = service.callback(request.args)
        if not user_key:
            user_key = models.Key(user_id=current_user.id,
                                  service_alias=service.alias)
        user_key.update(data)
        models.db.session.add(user_key)
        flash('Granted access to %s' % service.name, 'success')

    except OAuthError:
        flash('Error occurred while authorizing %s' % service.name, 'error')

    except OAuthDenied, e:
        # User denied the authorization request
        if user_key:
            models.db.session.delete(user_key)
        flash(e.args[0], 'error')

    models.db.session.commit()
    return redirect(url_for('services'))


@config.app.route('/<domain>/<path:path>', methods=['OPTIONS', 'GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
@config.app.route('/<domain>/', defaults={'path': u''}, methods=['OPTIONS', 'GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
def api(domain, path):
    # Allow clients to override the method being provided, in case the client
    # or network doesn't natively support PATCH. For example, Amazon discards
    # PATCH requests before they ever reach Heroku, much less foauth.org.
    if request.method == 'POST':
        override = request.headers.get('X-Http-Method-Override')
        if override == 'PATCH':
            request.environ['REQUEST_METHOD'] = override

    auth = request.authorization
    if auth:
        user = models.User.query.filter_by(email=auth.username).first()
        if user and user.check_password(auth.password):
            try:
                service = config.domain_map[domain]
            except KeyError:
                abort(404)

            key = user.keys.filter_by(service_alias=service.alias).first()
            if not key:
                abort(403)
            if key.is_expired():
                # Key has expired
                if key.refresh_token:
                    data = service.refresh_token(key.refresh_token)
                    key.update(data)
                    models.db.session.add(key)
                    models.db.session.commit()
                else:
                    # Unable to refresh the token
                    abort(403)
            resp = service.api(key, domain, path)
            content = resp.raw.read()

            if 'Transfer-Encoding' in resp.headers and \
               resp.headers['Transfer-Encoding'].lower() == 'chunked':
                # WSGI doesn't handle chunked encodings
                del resp.headers['Transfer-Encoding']
            if 'Connection' in resp.headers and \
               resp.headers['Connection'].lower() == 'keep-alive':
                # WSGI doesn't handle keep-alive
                del resp.headers['Connection']

            return config.app.make_response((content,
                                             resp.status_code,
                                             resp.headers))
    abort(403)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    config.app.run(host='0.0.0.0', port=port)
