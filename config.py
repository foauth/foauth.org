import glob
import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask_sslify import SSLify

from foauth.providers import OAuthMeta

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['DEBUG'] = 'DEBUG' in os.environ
app.wsgi_app = ProxyFix(app.wsgi_app)
SSLify(app, subdomains=True)


def get_service_modules():
    for filename in glob.glob(os.path.join('services', '*.py')):
        module_name = os.path.splitext(os.path.split(filename)[1])[0]
        if not module_name.startswith('__'):
            yield module_name


def get_oauth_providers(module_name):
    module = getattr(__import__('services.%s' % module_name), module_name)
    for name, obj in module.__dict__.items():
        if isinstance(obj, OAuthMeta):
            yield obj


services = []
for module_name in get_service_modules():
    for service in get_oauth_providers(module_name):
        alias = service.alias.upper()
        key = os.environ.get('%s_KEY' % alias, '').decode('utf8')
        secret = os.environ.get('%s_SECRET' % alias, '').decode('utf8')

        if key and secret:  # Only initialize if all the pieces are in place
            services.append(service(key, secret))


alias_map = {}
for service in services:
    alias_map[service.alias] = service

domain_map = {}
for service in services:
    for domain in service.api_domains:
        domain_map[domain] = service
