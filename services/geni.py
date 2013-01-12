import foauth.providers


class Geni(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://www.geni.com/'
    docs_url = 'http://www.geni.com/platform/developer/help/reference'
    category = 'Genealogy'

    # URLs to interact with the API
    authorize_url = 'https://www.geni.com/platform/oauth/authorize'
    access_token_url = 'https://www.geni.com/platform/oauth/request_token'
    api_domain = 'www.geni.com'

    available_permissions = [
        (None, 'read and write to your family tree'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/api/profile')
        print unicode(r.json()[u'guid'])
