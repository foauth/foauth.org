from oauthlib.oauth2.draft25 import utils
import foauth.providers


class Dailymile(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://dailymile.com'
    favicon_url = 'http://www.dailymile.com/favicon.ico'
    docs_url = 'http://www.dailymile.com/api/documentation'

    # URLs to interact with the API
    authorize_url = 'https://api.dailymile.com/oauth/authorize'
    access_token_url = 'https://api.dailymile.com/oauth/token'
    api_domain = 'api.dailymile.com'

    available_permissions = [
        (None, 'read and write to your workout data'),
    ]

    def bearer_type(self, token, r):
        r.url =  utils.add_params_to_uri(r.url, [((u'oauth_token', token))])
        return r

