import foauth.providers
from foauth import OAuthDenied, OAuthError


class Venmo(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://venmo.com/'
    docs_url = 'https://developer.venmo.com/docs/oauth'
    category = 'Money'

    # URLs to interact with the API
    authorize_url = 'https://api.venmo.com/v1/oauth/authorize'
    access_token_url = 'https://api.venmo.com/v1/oauth/access_token'
    api_domain = 'api.venmo.com'

    bearer_type = foauth.providers.BEARER_URI

    available_permissions = [
        (None, 'read your account details and current balance'),
        ('access_email', 'read your email address'),
        ('access_phone', 'read your phone number'),
        ('access_balance', 'read your current balance'),
        ('access_friends', 'access your list of friends'),
        ('access_feed', 'read your payment history and activity feed'),
    ]

    def get_authorize_params(self, redirect_uri, scopes):
        scopes = ['access_profile'] + scopes
        return super(Venmo, self).get_authorize_params(redirect_uri, scopes)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/v1/me')
        return unicode(r.json()[u'data'][u'user'][u'id'])
