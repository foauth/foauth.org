import foauth.providers


class Yammer(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://www.yammer.com/'
    docs_url = 'https://developer.yammer.com/api/'
    category = 'Social'

    # URLs to interact with the API
    authorize_url = 'https://www.yammer.com/dialog/oauth'
    access_token_url = 'https://www.yammer.com/oauth2/access_token.json'
    api_domain = 'www.yammer.com'

    available_permissions = [
        (None, 'read and post to your stream'),
    ]

    def parse_token(self, content):
        data = super(Yammer, self).parse_token(content)
        data['access_token'] = data['access_token']['token']
        return data
