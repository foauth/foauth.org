import foauth.providers
from foauth import OAuthDenied


class Twitter(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://www.twitter.com/'
    docs_url = 'https://dev.twitter.com/docs'

    # URLs to interact with the API
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    authorize_url = 'https://api.twitter.com/oauth/authorize'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    api_domain = 'api.twitter.com'

    available_permissions = [
        (None, 'read and send tweets, including DMs'),
    ]

    def callback(self, data):
        if 'denied' in data:
            raise OAuthDenied('Denied access to Twitter')

        return super(Twitter, self).callback(data)
