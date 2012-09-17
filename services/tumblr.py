import foauth.providers


class Tumblr(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.tumblr.com/'
    docs_url = 'http://www.tumblr.com/docs/en/api/v2'
    category = 'Blogs'

    # URLs to interact with the API
    request_token_url = 'http://www.tumblr.com/oauth/request_token'
    authorize_url = 'http://www.tumblr.com/oauth/authorize'
    access_token_url = 'http://www.tumblr.com/oauth/access_token'
    api_domain = 'api.tumblr.com'

    https = False

    available_permissions = [
        (None, 'read, write and manage your blog'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/v2/user/info')
        return r.json[u'response'][u'user'][u'name']
