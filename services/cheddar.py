from oauthlib.oauth2.draft25 import utils
import foauth.providers


class Cheddar(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://cheddarapp.com/'
    docs_url = 'https://cheddarapp.com/developer/'
    category = 'Tasks'

    # URLs to interact with the API
    authorize_url = 'https://api.cheddarapp.com/oauth/authorize'
    access_token_url = 'https://api.cheddarapp.com/oauth/token'
    api_domain = 'api.cheddarapp.com'

    available_permissions = [
        (None, 'read and write to your tasks'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/v1/me')
        return unicode(r.json[u'id'])
