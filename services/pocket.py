from werkzeug.urls import url_decode
import requests
import foauth.providers


class Pocket(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://getpocket.com/'
    docs_url = 'http://getpocket.com/developer/docs/overview'
    category = 'News'

    # URLs to interact with the API
    request_token_url = 'https://getpocket.com/v3/oauth/request'
    authorize_url = 'https://getpocket.com/auth/authorize'
    access_token_url = 'https://getpocket.com/v3/oauth/authorize'
    api_domain = 'getpocket.com'

    available_permissions = [
        (None, 'access your saved articles'),
    ]
    supports_state = False

    def get_authorize_params(self, redirect_uri, scopes):
        params = super(Pocket, self).get_authorize_params(redirect_uri, scopes)
        r = requests.post(self.request_token_url, data={
                'consumer_key': params['client_id'],
                'redirect_uri': redirect_uri,
            })
        data = url_decode(r.content)
        redirect_uri = '%s&code=%s' % (params['redirect_uri'], data['code'])
        return {
            'request_token': data['code'],
            'redirect_uri': redirect_uri,
        }

    def get_access_token_response(self, redirect_uri, data):
        return requests.post(self.get_access_token_url(), {
            'consumer_key': self.client_id,
            'code': data['code'],
            'redirect_uri': redirect_uri
        })

    def parse_token(self, content):
        data = url_decode(content)
        data['service_user_id'] = data['username']
        return data

    def bearer_type(self, token, r):
        r.prepare_url(r.url, {'consumer_key': self.client_id, 'access_token': token})
        return r
