import foauth.providers


class Trello(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://trello.com/'
    docs_url = 'https://trello.com/docs/api/'
    category = 'Tasks'

    # URLs to interact with the API
    request_token_url = 'https://trello.com/1/OAuthGetRequestToken'
    authorize_url = 'https://trello.com/1/OAuthAuthorizeToken'
    access_token_url = 'https://trello.com/1/OAuthGetAccessToken'
    api_domain = 'api.trello.com'

    available_permissions = [
        (None, 'read your projects'),
        ('write', 'read and write to your projects'),
        ('account', 'manage your account'),
    ]

    def get_authorize_params(self, redirect_uri, scopes):
        params = super(Trello, self).get_authorize_params(redirect_uri, scopes)
        params.update({
            'name': 'foauth.org', 'expiration': 'never',
            'scope': self.get_scope_string(['read'] + scopes),
        })
        return params

    def get_scope_string(self, scopes):
        return ','.join(scopes)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/1/members/me')
        return unicode(r.json()[u'id'])
