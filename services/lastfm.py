import flask
import hashlib
import itertools
import requests
from xml.dom import minidom

import foauth.providers


class LastFM(foauth.providers.OAuth2):
    # General info about the provider
    name = 'last.fm'
    provider_url = 'http://last.fm/'
    docs_url = 'http://www.last.fm/api/intro'
    category = 'Music'

    # URLs to interact with the API
    authorize_url = 'http://www.last.fm/api/auth/'
    access_token_url = 'http://ws.audioscrobbler.com/2.0/'
    api_domain = 'ws.audioscrobbler.com'

    available_permissions = [
        (None, 'read and manage your music history'),
    ]

    def parse_token(self, content):
        # Grab the key out of the XML
        dom = minidom.parseString(content)
        access_token = dom.getElementsByTagName('key')[0].firstChild.nodeValue
        return {'access_token': access_token}

    def get_authorize_params(self, *args, **kwargs):
        return {
            'api_key': self.client_id,
        }

    def callback(self, data, *args, **kwargs):
        auth = Session(self.client_id, self.client_secret, data['token'])
        params = {
            'method': 'auth.getSession',
            'api_key': self.client_id,
            'token': data['token'],
        }
        params['api_sig'] = auth.get_signature(params.items())
        resp = requests.get(self.access_token_url, params=params)

        return self.parse_token(resp.content)

    def authorize(self, scopes):
        redirect_uri = self.get_redirect_uri('callback')
        params = self.get_authorize_params(redirect_uri, scopes)
        req = requests.Request(self.authorize_url, params=params)
        return flask.redirect(req.full_url)

    def api(self, key, domain, path, method='GET', params=None, data=None,
            headers=None):
        url = 'http://%s%s' % (domain, path)
        auth = Session(self.client_id, self.client_secret, key.access_token)
        return requests.request(method, url, auth=auth, params=params or {},
                                data=data or {}, headers=headers or {})

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/2.0/?method=user.getInfo')
        dom = minidom.parseString(r.content)
        return dom.getElementsByTagName('id')[0].firstChild.nodeValue


class Session(object):
    def __init__(self, client_id, client_secret, token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token

    def __call__(self, r):
        params = r.params or r.data
        if hasattr(params, 'keys'):
            params = self.iterparams(params)
        signature = self.get_signature(params)
        r.params['sk'] = self.token
        r.params['api_key'] = self.client_id
        r.params['api_sig'] = signature
        return r

    def iterparams(self, params):
        # Pull the parameter values out of their lists,
        # yielding multiple values for a key if necessary.
        for key in params:
            for val in params[key]:
                yield (key, val)

    def get_signature(self, param_list):
        data = ''.join(i.encode('utf8') for i in itertools.chain(*sorted(param_list)))
        return hashlib.md5(data + self.client_secret).hexdigest()
