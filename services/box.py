import flask
import requests
import urllib
from xml.dom import minidom

import foauth.providers


class Box(foauth.providers.OAuth1):
    # General info about the provider
    name = 'Box'
    provider_url = 'https://www.box.com/'
    docs_url = 'http://developers.box.com/docs/'
    category = 'Files'

    # URLs to interact with the API
    request_token_url = 'https://api.box.com/1.0/rest'
    authorize_url = 'https://api.box.com/1.0/auth/%s'
    access_token_url = 'https://api.box.com/1.0/rest'
    api_domains = ['api.box.com', 'www.box.com']

    available_permissions = [
        (None, 'read and write to your files'),
    ]

    def get_ticket(self):
        params = {
            'action': 'get_ticket',
            'api_key': self.client_id,
        }
        resp = requests.post(self.get_request_token_url(), params=params)
        dom = minidom.parseString(resp.content)
        return dom.getElementsByTagName('ticket')[0].firstChild.nodeValue

    def authorize(self, scopes):
        return flask.redirect(self.authorize_url % self.get_ticket())

    def parse_token(self, content):
        dom = minidom.parseString(content)
        token = dom.getElementsByTagName('auth_token')[0].firstChild.nodeValue
        return {'access_token': token}

    def callback(self, data, *args, **kwargs):
        params = {
            'action': 'get_auth_token',
            'api_key': self.client_id,
            'ticket': data['ticket'],
            'token': data['auth_token'],
        }
        resp = requests.get(self.access_token_url, params=params)

        return self.parse_token(resp.content)

    def api(self, key, domain, path, method='GET', params=None, data=None,
            headers=None):
        url = 'https://%s%s' % (domain, path)
        auth = Auth(self.client_id, key.access_token)
        return requests.request(method, url, auth=auth, params=params or {},
                                data=data or {}, headers=dict(headers or {}))

    def get_user_id(self, key):
        r = self.api(key, self.api_domains[0], u'/2.0/folders/0')
        return r.json[u'owned_by'][u'id']


class Auth(object):
    def __init__(self, client_id, auth_token):
        self.client_id = client_id
        self.auth_token = auth_token

    def __call__(self, r):
        params = [('api_key', self.client_id), ('auth_token', self.auth_token)]
        r.headers['Authorization'] = 'BoxAuth %s' % urllib.urlencode(params)
        return r
