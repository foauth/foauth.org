import json
from os import urandom
import urllib
import urlparse

import flask
import requests
import requests.auth
from oauthlib.oauth1.rfc5849 import SIGNATURE_HMAC, SIGNATURE_TYPE_AUTH_HEADER
from oauthlib.oauth2.draft25 import tokens
from werkzeug.urls import url_decode

from foauth import OAuthError

BEARER = 'BEARER'
BEARER_HEADER = 'HEADER'
BEARER_BODY = 'BODY'
BEARER_URI = 'URI'
BEARER_TYPES = (BEARER_HEADER, BEARER_BODY, BEARER_URI)


class Bearer(object):
    def __init__(self, token, bearer_type=BEARER_HEADER):
        self.token = token

        if bearer_type in BEARER_TYPES or callable(bearer_type):
            self.bearer_type = bearer_type
        else:
            raise ValueError('Unknown bearer type %s' % bearer_type)

    def __call__(self, r):
        if self.bearer_type == BEARER_HEADER:
            r.headers = tokens.prepare_bearer_headers(self.token, r.headers)
        elif self.bearer_type == BEARER_BODY:
            r.data = tokens.prepare_bearer_body(self.token, r.data)
        elif self.bearer_type == BEARER_URI:
            r.url = tokens.prepare_bearer_uri(self.token, r.url)
        elif callable(self.bearer_type):
            r = self.bearer_type(self.token, r)

        return r


class OAuthMeta(type):
    def __init__(cls, name, bases, attrs):
        if 'alias' not in attrs:
            cls.alias = cls.__name__.lower()
        if 'api_domain' in attrs and 'api_domains' not in attrs:
            cls.api_domains = [cls.api_domain]
        if 'provider_url' in attrs and 'favicon_url' not in attrs:
            # Use a favicon service when no favicon is supplied
            primary = 'https://getfavicon.appspot.com/%s' % cls.provider_url
            domain = urlparse.urlparse(cls.provider_url).netloc
            backup = 'https://www.google.com/s2/favicons?domain=%s' % domain
            cls.favicon_url = '%s?defaulticon=%s' % (primary, urllib.quote(backup))

        if 'name' not in attrs:
            cls.name = cls.__name__


class OAuth(object):
    __metaclass__ = OAuthMeta

    https = True
    verify = True
    signature_method = SIGNATURE_HMAC
    signature_type = SIGNATURE_TYPE_AUTH_HEADER
    permissions_widget = 'checkbox'
    description = ''
    disclaimer = ''

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_request_token_url(self):
        return self.request_token_url

    def get_redirect_uri(self, url_name):
        root = flask.request.url_root
        path = flask.url_for(url_name, alias=self.alias)
        return urlparse.urljoin(root, path).decode('utf8')

    def get_scope_string(self, scopes):
        return ''

    def authorize(self, scopes):
        redirect_uri = self.get_redirect_uri('callback')
        params = self.get_authorize_params(redirect_uri=redirect_uri,
                                           scopes=scopes)
        req = requests.Request(self.authorize_url, params=params)
        return flask.redirect(req.full_url)

    def login(self):
        redirect_uri = self.get_redirect_uri('login_callback')
        params = self.get_authorize_params(redirect_uri=redirect_uri,
                                           scopes=[])
        req = requests.Request(self.authorize_url, params=params)
        return flask.redirect(req.full_url)

    # The remainder of the API must be implemented for each flavor of OAuth

    def callback(self, data, url_name):
        """
        Receives the full callback from the service and returns a 2-tuple
        containing the user token and user secret (if applicable).
        """
        raise NotImplementedError("callback() must be defined in a subclass")

    def api(self, key, domain, path, method='GET', params=None, data=None):
        """
        Passes along an API request to the service and returns the response.
        """
        raise NotImplementedError("api() must be defined in a subclass")


class OAuth1(OAuth):
    def parse_token(self, content):
        content = url_decode(content)
        return {
            'access_token': content['oauth_token'],
            'secret': content['oauth_token_secret'],
        }

    def get_request_token_params(self, redirect_uri, scopes):
        return {}

    def get_authorize_params(self, redirect_uri, scopes):
        auth = requests.auth.OAuth1(client_key=self.client_id,
                                    client_secret=self.client_secret,
                                    callback_uri=redirect_uri,
                                    signature_method=self.signature_method,
                                    signature_type=self.signature_type)
        resp = requests.post(self.get_request_token_url(), auth=auth,
                             params=self.get_request_token_params(redirect_uri, scopes),
                             headers={'Content-Length': '0'}, verify=self.verify)
        try:
            data = self.parse_token(resp.content)
        except Exception:
            raise OAuthError('Unable to parse access token')
        flask.session['%s_temp_secret' % self.alias] = data['secret']
        return {
            'oauth_token': data['access_token'],
            'oauth_callback': redirect_uri,
        }

    def callback(self, data, url_name):
        token = data['oauth_token']
        verifier = data.get('oauth_verifier', None)
        secret = flask.session['%s_temp_secret' % self.alias]
        del flask.session['%s_temp_secret' % self.alias]
        auth = requests.auth.OAuth1(client_key=self.client_id,
                                    client_secret=self.client_secret,
                                    resource_owner_key=token,
                                    resource_owner_secret=secret,
                                    verifier=verifier,
                                    signature_method=self.signature_method,
                                    signature_type=self.signature_type)
        resp = requests.post(self.access_token_url, auth=auth,
                             headers={'Content-Length': '0'}, verify=self.verify)
        try:
            return self.parse_token(resp.content)
        except Exception:
            raise OAuthError('Unable to parse access token')

    def api(self, key, domain, path, method='GET', params=None, data=None,
            headers=None):
        protocol = self.https and 'https' or 'http'
        url = '%s://%s%s' % (protocol, domain, path)
        auth = requests.auth.OAuth1(client_key=self.client_id,
                                    client_secret=self.client_secret,
                                    resource_owner_key=key.access_token,
                                    resource_owner_secret=key.secret,
                                    signature_method=self.signature_method,
                                    signature_type=self.signature_type)
        return requests.request(method, url, auth=auth, params=params or {},
                                data=data or {}, headers=headers or {},
                                verify=self.verify)


class OAuth2(OAuth):
    token_type = BEARER
    bearer_type = BEARER_HEADER
    supports_state = True

    def parse_token(self, content):
        return json.loads(content)

    def get_scope_string(self, scopes):
        return ' '.join(scopes)

    def get_authorize_params(self, redirect_uri, scopes):
        state = ''.join('%02x' % ord(x) for x in urandom(16))
        flask.session['%s_state' % self.alias] = state
        if not self.supports_state:
            redirect_uri += ('?state=%s' % state)
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'state': state,
        }
        if any(scopes):
            params['scope'] = self.get_scope_string(scopes)
        return params

    def callback(self, data, url_name):
        state = flask.session['%s_state' % self.alias]
        if 'state' in data and state != data['state']:
            flask.abort(403)
        del flask.session['%s_state' % self.alias]
        redirect_uri = self.get_redirect_uri(url_name)
        if not self.supports_state:
            redirect_uri += ('?state=%s' % state)
        resp = requests.post(self.access_token_url, {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': data['code'],
            'redirect_uri': redirect_uri
        }, verify=self.verify)

        return self.parse_token(resp.content)

    def refresh_token(self, token):
        resp = requests.post(self.access_token_url, {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': token
        }, verify=self.verify)

        return self.parse_token(resp.content)

    def api(self, key, domain, path, method='GET', params=None, data=None,
            headers=None):
        protocol = self.https and 'https' or 'http'
        url = '%s://%s%s' % (protocol, domain, path)
        if self.token_type == BEARER:
            auth = Bearer(key.access_token, bearer_type=self.bearer_type)
        return requests.request(method, url, auth=auth, params=params or {},
                                data=data or {}, headers=headers or {},
                                verify=self.verify)
