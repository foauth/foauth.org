import datetime
import flask
import hashlib
import itertools
import requests
from urlparse import urlparse, parse_qsl
from xml.dom import minidom

import foauth.providers


class Shutterfly(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://www.shutterfly.com/'
    docs_url = 'http://www.shutterfly.com/documentation/start.sfly'
    category = 'Pictures'

    # URLs to interact with the API
    authorize_url = 'http://www.shutterfly.com/oflyuser/grantApp.sfly'
    api_domain = 'ws.shutterfly.com'

    available_permissions = [
        (None, 'read and manage your photos and products'),
    ]

    def get_authorize_params(self, redirect_uri, scopes):
        auth = Session(self.client_id, self.client_secret)
        req = requests.Request(url=self.authorize_url, auth=auth, params={
            'oflyCallbackUrl': redirect_uri,
        })
        params = parse_qsl(urlparse(req.prepare().url).query)

        return params

    def callback(self, data, *args, **kwargs):
        return {
            'access_token': data['oflyUserid'],
        }

    def api(self, key, domain, path, method='GET', params=None, data=None,
            headers=None):
        url = 'https://%s%s' % (domain, path)
        auth = Session(self.client_id, self.client_secret, key.access_token)
        return requests.request(method, url, auth=auth, params=params or {},
                                data=data or {}, headers=headers or {})

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/user')
        dom = minidom.parseString(r.content)
        nodes = dom.getElementsByTagNameNS('http://openfly.shutterfly.com/v1.0', 'userid')
        return nodes[0].firstChild.nodeValue


class Session(object):
    def __init__(self, client_id, client_secret, token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token

    def __call__(self, r):
        if self.token:
            r.prepare_url(r.url, params={'oflyUserid': self.token})

        parsed_url = urlparse(r.url)
        path = parsed_url.path.rstrip('/')
        params = parse_qsl(parsed_url.query)

        timestamp = self.get_timestamp()
        call_params = [
            ('oflyAppId', self.client_id),
            ('oflyHashMeth', 'SHA1'),
            ('oflyTimestamp', timestamp),
        ]
        signature = self.get_signature(path, params, call_params)

        r.prepare_url(r.url, params=dict(call_params, oflyApiSig=signature))
        return r

    def get_timestamp(self):
        now = datetime.datetime.utcnow()
        return now.isoformat()[:23] + 'Z'

    def iterparams(self, params):
        # Pull the parameter values out of their lists,
        # yielding multiple values for a key if necessary.
        for key in params:
            for val in params[key]:
                yield (key, val)

    def encode_pair(self, key, value):
        return key.encode('utf8'), value.encode('utf8')

    def encode_params(self, params):
        return '&'.join('%s=%s' % self.encode_pair(*pair) for pair in params)

    def get_signature(self, path, params, call_params):
        data = self.encode_params(sorted(params))
        call_data = self.encode_params(call_params)
        data = '%s%s?%s&%s' % (self.client_secret, path, data, call_data)
        return hashlib.sha1(data).hexdigest()
