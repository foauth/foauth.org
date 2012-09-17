import foauth.providers


class Miso(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://gomiso.com/'
    docs_url = 'http://gomiso.com/developers/endpoints'
    category = 'Entertainment'

    # URLs to interact with the API
    request_token_url = 'http://gomiso.com/oauth/request_token'
    authorize_url = 'http://gomiso.com/oauth/authorize'
    access_token_url = 'http://gomiso.com/oauth/access_token'
    api_domain = 'gomiso.com'

    available_permissions = [
        (None, 'read and write to your TV history'),
    ]

    https = False

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/api/oauth/v1/users/show.json')
        return unicode(r.json[u'user'][u'id'])
