import foauth.providers


class PayPal(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://www.paypal.com/'
    docs_url = 'https://developer.paypal.com/webapps/developer/docs/api/'
    category = 'Money'

    # URLs to interact with the API
    authorize_url = 'https://www.paypal.com/webapps/auth/protocol/openidconnect/v1/authorize'
    access_token_url = 'https://api.paypal.com/v1/identity/openidconnect/tokenservice'
    api_domain = 'api.paypal.com'

    available_permissions = [
        (None, 'access your user ID'),
        ('profile', 'access your name, gender, date of birth and geographic region'),
        ('email', 'access your email address'),
        ('address', 'access your physical address information'),
        ('phone', 'access your phone number'),
        ('https://uri.paypal.com/services/paypalattributes', 'access your account information'),
    ]

    def get_authorize_params(self, redirect_uri, scopes):
        # We always need to at least request something
        scopes.append('openid')
        params = super(PayPal, self).get_authorize_params(redirect_uri, scopes)
        return params

    def parse_token(self, content):
        params = super(PayPal, self).parse_token(content)
        return params

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/v1/identity/openidconnect/userinfo/',
                     params={'schema': 'openid'})
        return unicode(r.json()[u'user_id'])
