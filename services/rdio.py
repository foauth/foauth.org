from werkzeug.urls import url_decode

import foauth.providers


class Rdio(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.rdio.com/'
    favicon_url = 'http://www.rdio.com/media/favicon_rdio_2012_11_15.ico'
    docs_url = 'http://developer.rdio.com/docs/REST/'
    category = 'Music'

    # URLs to interact with the API
    request_token_url = 'http://api.rdio.com/oauth/request_token'
    authorize_url = 'https://www.rdio.com/account/oauth1/authorize/'
    access_token_url = 'http://api.rdio.com/oauth/access_token'
    api_domain = 'api.rdio.com'

    available_permissions = [
        (None, 'access and manage your music'),
    ]

    https = False

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/1/', method='POST', data={
            'method': 'currentUser',
        })
        return unicode(r.json()[u'result'][u'key'])
