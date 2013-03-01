import flask
import hashlib
import itertools
import requests
from urlparse import urlparse, parse_qsl
from xml.dom import minidom

import foauth.providers


class RememberTheMilk(foauth.providers.OAuth2):
    # General info about the provider
    name = 'Remember the Milk'
    provider_url = 'http://rememberthemilk.com/'
    docs_url = 'https://www.rememberthemilk.com/services/api/'
    category = 'Tasks'

    # URLs to interact with the API
    authorize_url = 'http://www.rememberthemilk.com/services/auth/'
    access_token_url = 'http://api.rememberthemilk.com/services/rest/'
    api_domain = 'api.rememberthemilk.com'

    available_permissions = [
        (None, 'access your tasks, notes and contacts'),
        ('write', 'access, add and edit your tasks, notes and contacts'),
        ('delete', 'access, add, edit and delete your tasks, notes and contacts'),
    ]
    permissions_widget = 'radio'

    def parse_token(self, content):
        dom = minidom.parseString(content)
        access_token = dom.getElementsByTagName('token')[0].firstChild.nodeValue
        return {'access_token': access_token}

    def get_authorize_params(self, redirect_uri, scopes):
        params = {'api_key': self.client_id}

        if any(scopes):
            params['perms'] = scopes[0]
        else:
            params['perms'] = 'read'

        auth = Auth(self.client_id, self.client_secret, '')
        params['api_sig'] = auth.get_signature(params.items())
        return params

    def callback(self, data, *args, **kwargs):
        auth = Auth(self.client_id, self.client_secret, '')
        params = {
            'method': 'rtm.auth.getToken',
            'api_key': self.client_id,
            'frob': data['frob'],
        }
        params['api_sig'] = auth.get_signature(params.items())
        resp = requests.get(self.access_token_url, params=params)

        return self.parse_token(resp.content)

    def authorize(self, scopes):
        redirect_uri = self.get_redirect_uri('callback')
        params = self.get_authorize_params(redirect_uri, scopes)
        req = requests.Request(url=self.authorize_url, params=params)
        return flask.redirect(req.prepare().url)

    def api(self, key, domain, path, method='GET', params=None, data=None,
            headers=None):
        url = 'http://%s%s' % (domain, path)
        auth = Auth(self.client_id, self.client_secret, key.access_token)
        return requests.request(method, url, auth=auth, params=params or {},
                                data=data or {}, headers=headers or {})

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/services/rest/?method=rtm.auth.checkToken')
        dom = minidom.parseString(r.content)
        return dom.getElementsByTagName('user')[0].getAttribute('id')


class Auth(object):
    def __init__(self, client_id, client_secret, auth_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_token = auth_token

    def __call__(self, r):
        r.prepare_url(r.url, {'api_key': self.client_id, 'auth_token': self.token})
        if r.body:
            params = parse_sql(r.body)
        else:
            params = parse_qsl(urlparse(r.url).query)
        r.prepare_url(r.url, {'api_sig': self.get_signature(params)})
        return r

    def get_signature(self, param_list):
        data = ''.join(i.encode('utf8') for i in itertools.chain(*sorted(param_list)))
        return hashlib.md5(self.client_secret + data).hexdigest()
