from os import urandom
from urlparse import urljoin

import flask
import requests
import requests.auth
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

        if 'name' not in attrs:
            cls.name = cls.__name__


class OAuth(object):
    __metaclass__ = OAuthMeta

    https = True
    signature_method = requests.auth.SIGNATURE_HMAC
    signature_type = requests.auth.SIGNATURE_TYPE_AUTH_HEADER

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_request_token_url(self):
        return self.request_token_url

    def get_redirect_uri(self):
        root = flask.request.url_root
        path = flask.url_for('callback', alias=self.alias)
        return urljoin(root, path).decode('utf8')

    def get_scope_string(self, scopes):
        return ''

    def get_headers(self):
        return {}

    # The remainder of the API must be implemented for each flavor of OAuth

    def authorize(self):
        """
        Redirect the user to the service for authorization
        """
        raise NotImplementedError("authorize() must be defined in a subclass")

    def callback(self, data):
        """
        Receives the full callback from the service and returns a 2-tuple
        containing the user token and user secret (if applicable).
        """
        raise NotImplementedError("callback() must be defined in a subclass")

    def api(self, key, domain, path):
        """
        Passes along an API request to the service and returns the response.
        """
        raise NotImplementedError("api() must be defined in a subclass")


class OAuth1(OAuth):
    def parse_token(self, content):
        content = url_decode(content)
        return content['oauth_token'], content['oauth_token_secret']

    def get_authorize_params(self):
        auth = requests.auth.OAuth1(client_key=self.client_id,
                                    client_secret=self.client_secret,
                                    callback_uri=self.get_redirect_uri(),
                                    signature_method=self.signature_method,
                                    signature_type=self.signature_type)
        resp = requests.post(self.get_request_token_url(), auth=auth,
                             headers=self.get_headers())
        try:
            token, secret = self.parse_token(resp.content)
        except Exception:
            raise OAuthError('Unable to parse access token')
        flask.session['%s_temp_secret' % self.alias] = secret
        return {'oauth_token': token, 'oauth_callback': self.get_redirect_uri()}

    def authorize(self):
        params = self.get_authorize_params()
        req = requests.Request(self.authorize_url, params=params)
        return flask.redirect(req.full_url)

    def callback(self, data):
        token = data['oauth_token']
        verifier = data.get('oauth_verifier', None)
        secret = flask.session['%s_temp_secret' % self.alias]
        del flask.session['%s_temp_secret' % self.alias]
        auth = requests.auth.OAuth1(client_key=self.client_id,
                                    client_secret=self.client_secret,
                                    resource_owner_key=token,
                                    resource_owner_secret=secret,
                                    verifier=verifier,
        )
        if verifier:
            params = {'oauth_verifier': verifier}
        else:
            params = {'oauth_token': token}
        resp = requests.post(self.access_token_url, params=params, auth=auth,
                             headers=self.get_headers())
        try:
            return self.parse_token(resp.content)
        except Exception:
            raise OAuthError('Unable to parse access token')

    def api(self, key, domain, path):
        protocol = self.https and 'https' or 'http'
        url = '%s://%s/%s' % (protocol, domain, path)
        auth = requests.auth.OAuth1(client_key=self.client_id,
                                    client_secret=self.client_secret,
                                    resource_owner_key=key.key,
                                    resource_owner_secret=key.secret)
        return requests.request(flask.request.method, url, auth=auth,
                                data=flask.request.form or flask.request.data)


class OAuth2(OAuth):
    token_type = BEARER
    bearer_type = BEARER_HEADER
    supports_state = True

    def parse_token(self, content):
        # Must be specified in a subclass
        raise NotImplementedError("parse_token() must be defined in a subclass")

    def get_scope_string(self, scopes):
        return ' '.join(scopes)

    def get_authorize_params(self):
        state = ''.join('%02x' % ord(x) for x in urandom(16))
        flask.session['%s_state' % self.alias] = state
        redirect_uri = self.get_redirect_uri()
        if not self.supports_state:
            redirect_uri += ('?state=%s' % state)
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'state': state,
        }
        if any(s for (s, desc) in self.available_permissions):
            scopes = (s for (s, desc) in self.available_permissions if s)
            params['scope'] = self.get_scope_string(scopes)
        return params

    def authorize(self):
        params = self.get_authorize_params()
        req = requests.Request(self.authorize_url, params=params)
        return flask.redirect(req.full_url)

    def callback(self, data):
        state = flask.session['%s_state' % self.alias]
        if state != data['state']:
            abort(403)
        del flask.session['%s_state' % self.alias]
        redirect_uri = self.get_redirect_uri()
        if not self.supports_state:
            redirect_uri += ('?state=%s' % state)
        resp = requests.post(self.access_token_url, {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': data['code'],
            'redirect_uri': redirect_uri
        })

        # No secret is supplied for OAuth 2
        return self.parse_token(resp.content), ''

    def api(self, key, domain, path):
        protocol = self.https and 'https' or 'http'
        url = '%s://%s/%s' % (protocol, domain, path)
        return requests.request(flask.request.method, url, data=flask.request.data)
#        raise Exception(key, domain, path)

    def api(self, key, domain, path):
        protocol = self.https and 'https' or 'http'
        url = '%s://%s/%s' % (protocol, domain, path)
        if self.token_type == BEARER:
            auth = Bearer(key.key, bearer_type=self.bearer_type)
        return requests.request(flask.request.method, url, auth=auth,
                                data=flask.request.form or flask.request.data)


