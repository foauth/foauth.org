import urlparse

import foauth.providers
from oauthlib.oauth1.rfc5849 import SIGNATURE_TYPE_QUERY


class Netflix(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://www.netflix.com/'
    favicon_url = 'https://netflix.hs.llnwd.net/e1/en_US/icons/nficon.ico'
    docs_url = 'http://developer.netflix.com/docs'
    category = 'Movies/TV'

    # URLs to interact with the API
    request_token_url = 'http://api-public.netflix.com/oauth/request_token'
    authorize_url = 'https://api-user.netflix.com/oauth/login'
    access_token_url = 'http://api-public.netflix.com/oauth/access_token'
    api_domain = 'api-public.netflix.com'

    available_permissions = [
        (None, 'read and manage your queue'),
    ]

    https = False
    signature_type = SIGNATURE_TYPE_QUERY

    def get_authorize_params(self, *args, **kwargs):
        params = super(Netflix, self).get_authorize_params(*args, **kwargs)
        params['oauth_consumer_key'] = self.client_id
        return params

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/users/current',
                     params={'output': 'json'})
        redirect = r.json()[u'resource'][u'link'][u'href']
        parts = urlparse.urlparse(redirect)
        r = self.api(key, parts.netloc, parts.path,
                     params={'output': 'json'})
        return r.json()[u'user'][u'user_id']
