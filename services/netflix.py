import foauth.providers
from oauthlib.oauth1.rfc5849 import SIGNATURE_TYPE_QUERY


class Netflix(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://www.netflix.com/'
    docs_url = 'http://developer.netflix.com/docs'

    # URLs to interact with the API
    request_token_url = 'http://api.netflix.com/oauth/request_token'
    authorize_url = 'https://api-user.netflix.com/oauth/login'
    access_token_url = 'http://api.netflix.com/oauth/access_token'
    api_domains = ['api-public.netflix.com', 'api.netflix.com']

    available_permissions = [
        (None, 'read and manage your queue'),
    ]

    https = False
    signature_type = SIGNATURE_TYPE_QUERY

    def get_authorize_params(self, redirect_uri):
        params = super(Netflix, self).get_authorize_params(redirect_uri)
        params['oauth_consumer_key'] = self.client_id
        return params
