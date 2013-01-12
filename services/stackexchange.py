import os
from oauthlib.oauth2.draft25 import utils
from werkzeug.urls import url_decode
import foauth.providers


def token_uri(service, token, r):
    params = [((u'access_token', token)), ((u'key', service.app_key))]
    r.url = utils.add_params_to_uri(r.url, params)
    return r


class StackExchange(foauth.providers.OAuth2):
    # General info about the provider
    name = 'Stack Exchange'
    provider_url = 'https://stackexchange.com/'
    docs_url = 'https://api.stackexchange.com/docs'
    category = 'Questions'

    # URLs to interact with the API
    authorize_url = 'https://stackexchange.com/oauth'
    access_token_url = 'https://stackexchange.com/oauth/access_token'
    api_domain = 'api.stackexchange.com'

    available_permissions = [
        (None, 'read your user information'),
        ('read_inbox', 'read your global inbox'),
        ('no_expiry', 'access your data indefinitely'),
    ]

    bearer_type = token_uri

    def __init__(self, *args, **kwargs):
        super(StackExchange, self).__init__(*args, **kwargs)

        # StackExchange also uses an application key
        self.app_key = os.environ.get('STACKEXCHANGE_APP_KEY', '').decode('utf8')

    def parse_token(self, content):
        data = url_decode(content)
        data['expires_in'] = data.get('expires', None)
        return data

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/2.0/me/associated')
        return unicode(r.json()[u'items'][0][u'account_id'])
