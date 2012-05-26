import foauth.providers


class Flickr(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.flickr.com/'
    favicon_url = 'http://l.yimg.com/g/favicon.ico'
    docs_url = 'http://www.flickr.com/services/api/'

    # URLs to interact with the API
    request_token_url = 'http://www.flickr.com/services/oauth/request_token'
    authorize_url = 'http://www.flickr.com/services/oauth/authorize'
    access_token_url = 'http://www.flickr.com/services/oauth/access_token'
    api_domain = 'api.flickr.com'

    available_permissions = [
        # (None, 'access only your public photos'),
        # ('read', 'access your public and private photos'),
        # ('write', 'upload, edit and replace your photos'),
        ('delete', 'upload, edit, replace and delete your photos'),
    ]

    def get_authorize_params(self):
        params = super(Flickr, self).get_authorize_params()
        params['perms'] = self.available_permissions[0]
        return params

    def get_headers(self):
        return {'Content-Length': '0'}

