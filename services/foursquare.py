from oauthlib.oauth2.draft25 import utils
import foauth.providers


class Foursquare(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://www.foursquare.com/'
    favicon_url = 'https://static-s.foursquare.com/favicon-c62b82f6120e2c592a3e6f3476d66554.ico'
    docs_url = 'https://developer.foursquare.com/overview/'

    # URLs to interact with the API
    authorize_url = 'https://foursquare.com/oauth2/authorize'
    access_token_url = 'https://foursquare.com/oauth2/access_token'
    api_domain = 'api.foursquare.com'

    available_permissions = [
        (None, 'read and write to your check-ins'),
    ]

    def bearer_type(self, token, r):
        r.url =  utils.add_params_to_uri(r.url, [((u'oauth_token', token))])
        return r

