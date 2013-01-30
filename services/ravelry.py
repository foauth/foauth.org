import foauth.providers


class Ravelry(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.ravelry.com/'
    docs_url = 'http://www.ravelry.com/groups/ravelry-api/pages/API-Documentation'
    category = 'Crafts'

    # URLs to interact with the API
    request_token_url = 'https://www.ravelry.com/oauth/request_token'
    authorize_url = 'https://www.ravelry.com/oauth/authorize'
    access_token_url = 'https://www.ravelry.com/oauth/access_token'
    api_domain = 'api.ravelry.com'

    available_permissions = [
        (None, 'read and write to your knitting data'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/current_user.json')
        return unicode(r.json()[u'user'][u'id'])
