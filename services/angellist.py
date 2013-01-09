import foauth.providers


class AngelList(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://angel.co/'
    docs_url = 'https://angel.co/api'
    category = 'Money'

    # URLs to interact with the API
    authorize_url = 'https://angel.co/api/oauth/authorize'
    access_token_url = 'https://angel.co/api/oauth/token'
    api_domain = 'api.angel.co'

    available_permissions = [
        (None, 'follow items and update your status'),
        ('email', 'access your email address'),
        ('message', 'read and send private messages'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/1/me')
        return unicode(r.json[u'id'])
