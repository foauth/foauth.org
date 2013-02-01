import flask
import foauth.providers


class GetGlue(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://getglue.com/'
    docs_url = 'http://getglue.com/api'
    category = 'Movies/TV'

    # URLs to interact with the API
    request_token_url = 'https://api.getglue.com/oauth/request_token'
    authorize_url = 'http://getglue.com/oauth/authorize'
    access_token_url = 'https://api.getglue.com/oauth/access_token'
    api_domain = 'api.getglue.com'

    available_permissions = [
        (None, 'read and write your social checkins'),
    ]

    returns_token = False

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/v2/user/profile?format=json')
        return r.json()[u'profile'][u'username']
