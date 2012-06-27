from werkzeug.urls import url_decode
from oauthlib.oauth1.rfc5849 import SIGNATURE_TYPE_BODY

import foauth.providers


class Rdio(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.rdio.com/'
    docs_url = 'http://developer.rdio.com/docs/REST/'

    # URLs to interact with the API
    request_token_url = 'http://api.rdio.com/oauth/request_token'
    authorize_url = None  # Provided when the request token is granted
    access_token_url = 'http://api.rdio.com/oauth/access_token'
    api_domain = 'api.rdio.com'

    available_permissions = [
        (None, 'access and manage your music'),
    ]

    def parse_token(self, content):
        # Override standard token request to also get the authorization URL
        data = url_decode(content)
        if 'login_url' in data:
            self.authorize_url = data['login_url']
        return super(Rdio, self).parse_token(content)

