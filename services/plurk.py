import foauth.providers


class Plurk(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.plurk.com/'
    docs_url = 'http://www.plurk.com/API#toc'
    category = 'Social'

    # URLs to interact with the API
    request_token_url = 'https://www.plurk.com/OAuth/request_token'
    authorize_url = 'http://www.plurk.com/OAuth/authorize'
    access_token_url = 'https://www.plurk.com/OAuth/access_token'
    api_domain = 'www.plurk.com'

    available_permissions = [
        (None, 'access and update your profile and plurks'),
    ]

    https = False

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/APP/Users/currUser')
        return unicode(r.json[u'id'])
