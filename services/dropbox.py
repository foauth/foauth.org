import foauth.providers
from oauthlib.oauth1.rfc5849 import SIGNATURE_PLAINTEXT


class Dropbox(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://www.dropbox.com/'
    docs_url = 'https://www.dropbox.com/developers/reference/api'
    category = 'Files'

    # URLs to interact with the API
    request_token_url = 'https://api.dropbox.com/1/oauth/request_token'
    authorize_url = 'https://www.dropbox.com/1/oauth/authorize'
    access_token_url = 'https://api.dropbox.com/1/oauth/access_token'
    api_domains = ['api.dropbox.com', 'api-content.dropbox.com']

    signature_method = SIGNATURE_PLAINTEXT

    available_permissions = [
        (None, 'read and write to your entire Dropbox'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domains[0], u'/1/account/info')
        return unicode(r.json()[u'uid'])
