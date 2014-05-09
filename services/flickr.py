import foauth.providers


class Flickr(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.flickr.com/'
    docs_url = 'http://www.flickr.com/services/api/'
    category = 'Pictures'

    # URLs to interact with the API
    request_token_url = 'http://www.flickr.com/services/oauth/request_token'
    authorize_url = 'http://www.flickr.com/services/oauth/authorize'
    access_token_url = 'http://www.flickr.com/services/oauth/access_token'
    api_domain = 'api.flickr.com'

    available_permissions = [
        (None, 'access your public and private photos'),
        ('write', 'upload, edit and replace your photos'),
        ('delete', 'upload, edit, replace and delete your photos'),
    ]
    permissions_widget = 'radio'

    def get_authorize_params(self, redirect_uri, scopes):
        params = super(Flickr, self).get_authorize_params(redirect_uri, scopes)
        params['perms'] = scopes[0] or 'read'
        return params

    def get_user_id(self, key):
        url = u'/services/rest/?method=flickr.people.getLimits'
        url += u'&format=json&nojsoncallback=1'
        r = self.api(key, self.api_domain, url)
        return r.json()[u'person'][u'nsid']
