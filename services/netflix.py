import foauth.providers


class Netflix(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://www.netflix.com/'
    favicon_url = 'https://netflix.hs.llnwd.net/e1/us/icons/nficon.ico'
    docs_url = 'http://developer.netflix.com/docs'

    # URLs to interact with the API
    request_token_url = 'http://api.netflix.com/oauth/request_token'
    authorize_url = 'https://api-user.netflix.com/oauth/login'
    access_token_url = 'http://api.netflix.com/oauth/access_token'
    api_domain = 'api.netflix.com'

    available_permissions = [
        (None, 'read and manage your queue'),
    ]

    def get_authorize_params(self):
        params = super(Netflix, self).get_authorize_params()
        params['oauth_consumer_key'] = self.client_id
        return params
