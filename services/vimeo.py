import foauth.providers


class Vimeo(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://vimeo.com/'
    docs_url = 'http://developer.vimeo.com/apis/advanced'
    category = 'Videos'

    # URLs to interact with the API
    request_token_url = 'https://vimeo.com/oauth/request_token'
    authorize_url = 'https://vimeo.com/oauth/authorize'
    access_token_url = 'https://vimeo.com/oauth/access_token'
    api_domain = 'vimeo.com'

    available_permissions = [
        (None, 'access your videos'),
        ('write', 'access, update and like videos'),
        ('delete', 'access, update, like and delete videos'),
    ]
    permissions_widget = 'radio'

    def get_authorize_params(self, redirect_uri, scopes):
        params = super(Vimeo, self).get_authorize_params(redirect_uri, scopes)

        if any(scopes):
            params['permission'] = scopes[0]

        return params

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/api/rest/v2?method=vimeo.people.getInfo&format=json')
        return r.json[u'person'][u'id']
