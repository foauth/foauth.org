import foauth.providers


class Imgur(foauth.providers.OAuth2):
    # General info about the provider
    name = 'imgur'
    provider_url = 'http://imgur.com/'
    docs_url = 'http://api.imgur.com/'
    category = 'Pictures'

    # URLs to interact with the API
    authorize_url = 'https://api.imgur.com/oauth2/authorize'
    access_token_url = 'https://api.imgur.com/oauth2/token'
    api_domain = 'api.imgur.com'

    available_permissions = [
        (None, 'read and write to your images'),
    ]

    # This is hopefully a short-term fix to a hostname mismatch on their end
    verify = False

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/3/account/me.json')
        return unicode(r.json()[u'data'][u'id'])
