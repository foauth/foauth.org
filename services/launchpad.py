from oauthlib.oauth1.rfc5849 import SIGNATURE_PLAINTEXT, SIGNATURE_TYPE_BODY, SIGNATURE_TYPE_AUTH_HEADER
import requests

import foauth.providers

class Launchpad(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://launchpad.net/'
    docs_url = 'https://launchpad.net/+apidoc/1.0.html'
    category = 'Code'

    # URLs to interact with the API
    request_token_url = 'https://launchpad.net/+request-token'
    authorize_url = 'https://launchpad.net/+authorize-token'
    access_token_url = 'https://launchpad.net/+access-token'
    api_domains = ['api.launchpad.net', 'api.staging.launchpad.net']

    signature_method = SIGNATURE_PLAINTEXT
    returns_token = False
    signature_type = SIGNATURE_TYPE_AUTH_HEADER

    available_permissions = [
        (None, 'read non-privade data'),
        ('WRITE_PUBLIC', 'change non-private data'),
        ('READ_PRIVATE', 'read anything, including private data'),
        ('WRITE_PRIVATE', 'change anything, including private data'),
    ]
    permissions_widget = 'radio'

    def __init__(self, *args, **kwargs):
        super(Launchpad, self).__init__(*args, **kwargs)
        self.client_secret = ''  # Must be empty to satisfy Launchpad

    def get_authorize_params(self, redirect_uri, scopes):
        params = super(Launchpad, self).get_authorize_params(redirect_uri, scopes)
        params['allow_permission'] = scopes[0] or 'READ_PUBLIC'
        return params

    def get_request_token_response(self, redirect_uri, scopes):
        # Launchpad expects the signature in the body, but we don't have
        # additional parameters, so oauthlib doesn't help us here.
        return requests.post(self.get_request_token_url(),
                             data={'oauth_consumer_key': self.client_id,
                                   'oauth_signature_method': 'PLAINTEXT',
                                   'oauth_signature': '&'})

    def get_access_token_response(self, token, secret, verifier=None):
        # Launchpad expects the signature in the body, but we don't have
        # additional parameters, so oauthlib doesn't help us here.
        req = requests.Request(url=self.authorize_url,
                               data={'oauth_consumer_key': self.client_id,
                                     'oauth_token': token,
                                     'oauth_signature_method': 'PLAINTEXT',
                                     'oauth_signature': '&%s' % secret})
        req = req.prepare()
        return requests.post(self.get_access_token_url(),
                             data={'oauth_consumer_key': self.client_id,
                                   'oauth_token': token,
                                   'oauth_signature_method': 'PLAINTEXT',
                                   'oauth_signature': '&%s' % secret})

    def get_user_id(self, key):
        r = super(Launchpad, self).api(key, self.api_domains[0], '/1.0/people/+me')
        return r.json()[u'name']
