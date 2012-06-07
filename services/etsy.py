from werkzeug.urls import url_decode

import foauth.providers


class Etsy(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.etsy.com/'
    favicon_url = 'http://www.etsy.com/images/favicon.ico'
    docs_url = 'http://www.etsy.com/developers/documentation'

    # URLs to interact with the API
    request_token_url = 'http://openapi.etsy.com/v2/oauth/request_token'
    authorize_url = None  # Provided when the request token is granted
    access_token_url = 'http://openapi.etsy.com/v2/oauth/access_token'
    api_domain = 'openapi.etsy.com'

    available_permissions = [
        (None, 'read your profile information and public listings'),
        ('email_r', 'read your email address'),
        ('listings_r', 'read your inactive and expired (i.e., non-public) listings'),
        ('listings_w', 'create and edit your listings'),
        ('listings_d', 'delete your listings'),
        ('transactions_r', 'read your purchase and sales data'),
        ('transactions_w', 'update your sales data'),
        ('billing_r', 'read your Etsy bill charges and payments'),
        ('profile_r', 'read your private profile information'),
        ('profile_w', 'update your private profile information'),
        ('address_r', 'read your shipping address'),
        ('address_w', 'update and delete your shipping address'),
        ('favorites_rw', 'add to and remove from your favorite listings and users'),
        ('shops_rw', 'update your shop description, messages and sections'),
        ('cart_rw', 'add and remove listings from your shopping cart'),
        ('recommend_rw', 'view, accept and reject your recommended listings'),
        ('feedback_r', 'view all details of your feedback (including history)'),
        ('treasury_w', 'create and delete treasuries and treasury comments'),
    ]

    def get_request_token_url(self):
        # Override standard request token URL in order to add permissions
        url = super(Etsy, self).get_request_token_url()
        perms = (p for (p, desc) in self.available_permissions if p)
        return '%s?scope=%s' % (url, ' '.join(perms))

    def parse_token(self, content):
        # Override standard token request to also get the authorization URL
        data = url_decode(content)
        if 'login_url' in data:
            self.authorize_url = data['login_url']
        return data['oauth_token'], data['oauth_token_secret'], None

