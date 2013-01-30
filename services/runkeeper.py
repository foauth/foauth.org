import foauth.providers


class Runkeeper(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://runkeeper.com/'
    docs_url = 'http://developer.runkeeper.com/healthgraph/overview'
    category = 'Fitness'

    # URLs to interact with the API
    authorize_url = 'https://runkeeper.com/apps/authorize'
    access_token_url = 'https://runkeeper.com/apps/token'
    api_domain = 'api.runkeeper.com'

    available_permissions = [
        (None, 'access your health and fitness data'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domains[0], u'/user')
        return unicode(r.json()[u'userID'])
