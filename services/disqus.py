from oauthlib.oauth2.draft25 import utils
import foauth.providers


def token_uri(service, token, r):
    params = [((u'access_token', token)), ((u'api_key', service.client_id))]
    r.url =  utils.add_params_to_uri(r.url, params)
    return r


class Disqus(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://disqus.com/'
    docs_url = 'http://disqus.com/api/docs/'

    # URLs to interact with the API
    authorize_url = 'https://disqus.com/api/oauth/2.0/authorize/'
    access_token_url = 'https://disqus.com/api/oauth/2.0/access_token/'
    api_domain = 'disqus.com'

    available_permissions = [
        (None, 'read data on your behalf'),
        ('write', 'write data on your behalf'),
        ('admin', 'moderate your forums'),
    ]

    bearer_type = token_uri

    def get_scope_string(self, scopes):
        # Disqus doesn't follow the spec on this point
        return ','.join(scopes)

