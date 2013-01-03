from oauthlib.oauth2.draft25 import utils
import foauth.providers


class Foursquare(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://www.foursquare.com/'
    docs_url = 'https://developer.foursquare.com/overview/'
    category = 'Travel'

    # URLs to interact with the API
    authorize_url = 'https://foursquare.com/oauth2/authorize'
    access_token_url = 'https://foursquare.com/oauth2/access_token'
    api_domain = 'api.foursquare.com'

    available_permissions = [
        (None, 'read and write to your check-ins'),
    ]

    def bearer_type(self, token, r):
        r.url = utils.add_params_to_uri(r.url, [((u'oauth_token', token))])
        return r

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/v2/users/self')
        return r.json[u'response'][u'user'][u'id']
