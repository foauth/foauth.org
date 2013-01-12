import foauth.providers


def draft10(service, token, r):
    headers = r.headers or {}
    headers[u'Authorization'] = u'OAuth %s' % token
    r.headers = headers
    return r


class DeviantArt(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://deviantart.com/'
    docs_url = 'http://www.deviantart.com/developers/'
    category = 'Pictures'

    # URLs to interact with the API
    authorize_url = 'https://www.deviantart.com/oauth2/draft15/authorize'
    access_token_url = 'https://www.deviantart.com/oauth2/draft15/token'
    api_domain = 'www.deviantart.com'

    available_permissions = [
        (None, 'read and write to your artwork'),
    ]

    bearer_type = draft10

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/api/draft15/user/whoami')
        return r.json()[u'username']
