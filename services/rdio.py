from werkzeug.urls import url_decode
from oauthlib.oauth1.rfc5849 import SIGNATURE_TYPE_BODY

import foauth.providers


class Rdio(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.rdio.com/'
    favicon_url = 'http://ak.rdio.com/media/images/icons/Rdio_32.png'
    docs_url = 'http://developer.rdio.com/docs/REST/'

    # URLs to interact with the API
    request_token_url = 'http://api.rdio.com/oauth/request_token'
    authorize_url = None  # Provided when the request token is granted
    access_token_url = 'http://api.rdio.com/oauth/access_token'
    api_domain = 'api.rdio.com'

    available_permissions = [
        (None, 'access and manage your music'),
    ]

#    signature_type = SIGNATURE_TYPE_BODY

    def parse_token(self, content):
        print 'Parsing token!'
        # Override standard token request to also get the authorization URL
        data = url_decode(content)
        print data
        if 'login_url' in data:
            self.authorize_url = data['login_url']
        return data['oauth_token'], data['oauth_token_secret'], None

