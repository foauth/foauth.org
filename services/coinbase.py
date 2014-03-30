from oauthlib.common import add_params_to_uri
import foauth.providers


class Coinbase(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://coinbase.com/'
    docs_url = 'https://coinbase.com/api/doc'
    category = 'Money'

    # URLs to interact with the API
    authorize_url = 'https://coinbase.com/oauth/authorize'
    access_token_url = 'https://coinbase.com/oauth/token'
    api_domain = 'coinbase.com'

    available_permissions = [
        (None, 'View your basic account information'),
        ('merchant', 'Create payment buttons and forms, view your basic user information, edit your merchant settings, and generate new receive addresses'),
        ('balance', 'View your balance'),
        ('addresses', 'View receive addresses and create new ones'),
        ('buttons', 'Create payment buttons'),
        ('buy', 'Buy bitcoin'),
        ('contacts', 'List emails and bitcoin addresses in your contact list'),
        ('orders', 'List merchant orders received'),
        ('sell', 'Sell bitcoin'),
        ('transactions', 'View your transaction history'),
        ('send', 'Debit an unlimited amount of money from your account'),
        ('request', 'Request money from your account'),
        ('transfers', 'List bitcoin buy and sell history'),
        ('recurring_payments', 'List your recurring payments'),
        ('oauth_apps', "List the other apps you've authorized"),
        ('all', 'All of the above'),
    ]

    def get_authorize_params(self, redirect_uri, scopes):
        # Always request at least user information
        scopes.append('user')
        return super(Coinbase, self).get_authorize_params(redirect_uri, scopes)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/api/v1/users')
        return r.json()[u'users'][0][u'user'][u'id']
