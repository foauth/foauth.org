import json
import requests

import foauth.providers


class Untappd(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://untappd.com/'
    docs_url = 'https://untappd.com/api/docs'
    favicon_url = provider_url + 'favicon.ico'
    category = 'Food/Drink'

    # URLs to interact with the API
    authorize_url = 'https://untappd.com/oauth/authenticate/'
    access_token_url = 'https://untappd.com/oauth/authorize/'
    api_domain = 'api.untappd.com'

    available_permissions = [
        (None, 'read and write to your social drinking'),
    ]

    bearer_type = foauth.providers.BEARER_URI

    def get_authorize_params(self, redirect_uri, scopes):
        params = super(Untappd, self).get_authorize_params(redirect_uri, scopes)
        params['redirect_url'] = params.pop('redirect_uri')
        return params

    def get_access_token_response(self, redirect_uri, data):
        return requests.get(self.get_access_token_url(), params={
                                'client_id': self.client_id,
                                'client_secret': self.client_secret,
                                'response_type': 'code',
                                'code': data['code'],
                                'redirect_url': redirect_uri,
                            }, verify=self.verify, auth=self.auth)

    def parse_token(self, content):
        return json.loads(content)[u'response']

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/v4/user/info')
        return unicode(r.json()[u'response'][u'user'][u'id'])
