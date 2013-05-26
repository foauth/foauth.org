import foauth.providers


class Assembla(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://www.assembla.com/'
    docs_url = 'http://api-doc.assembla.com/content/api_reference.html'
    category = 'Code'

    # URLs to interact with the API
    authorize_url = 'https://api.assembla.com/authorization'
    access_token_url = 'https://api.assembla.com/token'
    api_domain = 'api.assembla.com'

    available_permissions = [
        (None, 'read, write and manage your projects'),
    ]

    def __init__(self, *args, **kwargs):
        super(Assembla, self).__init__(*args, **kwargs)
        self.auth = (self.client_id, self.client_secret)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/v1/user')
        return unicode(r.json()[u'id'])
