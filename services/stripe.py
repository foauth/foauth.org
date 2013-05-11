import foauth.providers
from foauth import OAuthDenied, OAuthError


class Stripe(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://stripe.com/'
    docs_url = 'https://stripe.com/docs/api'
    category = 'Money'

    # URLs to interact with the API
    authorize_url = 'https://connect.stripe.com/oauth/authorize'
    access_token_url = 'https://connect.stripe.com/oauth/token'
    api_domain = 'api.stripe.com'

    available_permissions = [
        (None, 'read your account and payment history'),
        ('read_write', 'read and write to your account and payments'),
    ]
    permissions_widget = 'radio'

    def get_authorize_params(self, redirect_uri, scopes):
        params = super(Stripe, self).get_authorize_params(redirect_uri, scopes)
        params['stripe_landing'] = 'login'
        return params

    def callback(self, data, *args, **kwargs):
        if data.get('error', '') == 'access_denied':
            raise OAuthDenied('Denied access to Stripe')

        return super(Stripe, self).callback(data, *args, **kwargs)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/v1/account')
        return unicode(r.json()[u'id'])
