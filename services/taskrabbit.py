from oauthlib.oauth2.draft25 import utils
import foauth.providers


class Taskrabbit(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://www.taskrabbit.com/'
    docs_url = 'http://taskrabbit.github.com/'
    category = 'Tasks'

    # URLs to interact with the API
    # These are temporary until Taskrabbit approves foauth for production use
    authorize_url = 'https://taskrabbitdev.com/api/authorize'
    access_token_url = 'https://taskrabbitdev.com/api/oauth/token'
    api_domain = 'taskrabbitdev.com'

    available_permissions = [
        (None, 'read and write to your tasks'),
    ]

    def get_authorize_params(self, *args, **kwargs):
        params = super(Taskrabbit, self).get_authorize_params(*args, **kwargs)

        # Prevent the request for credit card information
        params['card'] = 'false'

        return params

    def bearer_type(self, token, r):
        r.headers['Authorization'] = 'OAuth %s' % token
        return r

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/api/v1/account')
        return r.json[u'id']
