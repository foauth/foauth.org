import foauth.providers


class Wordpress(foauth.providers.OAuth2):
    # General info about the provider
    name = 'WordPress.com'
    provider_url = 'https://www.wordpress.com/'
    docs_url = 'http://developer.wordpress.com/docs/api/'
    category = 'Blogs'

    # URLs to interact with the API
    authorize_url = 'https://public-api.wordpress.com/oauth2/authorize'
    access_token_url = 'https://public-api.wordpress.com/oauth2/token'
    api_domain = 'public-api.wordpress.com'

    available_permissions = [
        (None, 'read and post to your blog'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/rest/v1/me')
        return unicode(r.json[u'ID'])
