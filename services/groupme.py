import flask
import foauth.providers


class GroupMe(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://groupme.com/'
    docs_url = 'http://dev.groupme.com/docs/v3'
    category = 'Social'

    # URLs to interact with the API
    authorize_url = 'https://api.groupme.com/oauth/authorize'
    api_domain = 'api.groupme.com'

    available_permissions = [
        (None, 'access and manage your profile and messages'),
    ]

    def get_authorize_params(self, redirect_uri, scopes):
        return {'client_id': self.client_id}

    def callback(self, data, url_name):
        # The access token comes back directly in the callback
        return data

    def bearer_type(self, token, r):
        r.headers['X-Access-Token'] = token
        return r

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/v3/users/me')
        return unicode(r.json()[u'response'][u'id'])
