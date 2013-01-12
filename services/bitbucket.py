import foauth.providers


class Bitbucket(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://bitbucket.org/'
    docs_url = 'http://confluence.atlassian.com/display/BITBUCKET/Using+the+Bitbucket+REST+APIs'
    category = 'Code'

    # URLs to interact with the API
    request_token_url = 'https://bitbucket.org/api/1.0/oauth/request_token/'
    authorize_url = 'https://bitbucket.org/api/1.0/oauth/authenticate/'
    access_token_url = 'https://bitbucket.org/api/1.0/oauth/access_token/'
    api_domain = 'api.bitbucket.org'

    available_permissions = [
        (None, 'read and write your code and issues'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/1.0/user/')
        return r.json()[u'user'][u'username']
