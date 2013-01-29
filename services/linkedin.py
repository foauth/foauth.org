import foauth.providers
from foauth import OAuthDenied


class LinkedIn(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.linkedin.com/'
    docs_url = 'https://developer.linkedin.com/documents/linkedin-api-resource-map'
    category = 'Career'

    # URLs to interact with the API
    request_token_url = 'https://api.linkedin.com/uas/oauth/requestToken'
    authorize_url = 'https://www.linkedin.com/uas/oauth/authorize'
    access_token_url = 'https://api.linkedin.com/uas/oauth/accessToken'
    api_domain = 'api.linkedin.com'

    available_permissions = [
        (None, 'read and write to your employment information'),
    ]

    def callback(self, data, *args, **kwargs):
        if data.get('oauth_problem', '') == 'user_refused':
            raise OAuthDenied('Denied access to LinkedIn')

        return super(LinkedIn, self).callback(data, *args, **kwargs)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/v1/people/~:(id)?format=json')
        return r.json()[u'id']
