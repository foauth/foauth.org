import foauth.providers


class Vimeo(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://vimeo.com/'
    docs_url = 'http://developer.vimeo.com/apis/advanced'
    category = 'Videos'

    # URLs to interact with the API
    request_token_url = 'https://vimeo.com/oauth/request_token'
    authorize_url = 'https://vimeo.com/oauth/authorize?permission=delete'
    access_token_url = 'https://vimeo.com/oauth/access_token'
    api_domain = 'vimeo.com'

    available_permissions = [
        ('read', 'access information about videos'),
        ('write', 'update and like videos'),
        ('delete', 'delete videos'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/api/rest/v2?method=vimeo.people.getInfo&format=json')
        return r.json[u'person'][u'id']
