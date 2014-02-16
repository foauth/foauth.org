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

        # Permissions in all-caps are provided through PayPal's separate permissions API
        ('EXPRESS_CHECKOUT', 'use Express Checkout to process payments'),
        ('DIRECT_PAYMENT', 'process debit card payments'),
        ('SETTLEMENT_CONSOLIDATION', 'consolidate funds from child accounts into a master account'),
        ('SETTLEMENT_REPORTING', 'provide reporting for consolidated funds'),
        ('AUTH_CAPTURE', 'authorize and capture transactions'),
        ('MOBILE_CHECKOUT', 'use Express Checkout to process mobile payments'),
        ('AIR_TRAVEL', 'authorize transactions with Universal Air Travel Plans'),
        ('TRANSACTION_SEARCH', 'search through your transactions'),
        ('RECURRING_PAYMENTS', 'create and manage recurring payments'),
        ('REFUND', 'refund a transaction on your behalf'),
        ('BUTTON_MANAGER', 'create and manage payment buttons on your behalf'),
        ('MANAGE_PENDING_TRANSACTION_STATUS', 'accept or deny a pending transaction'),
        ('RECURRING_PAYMENT_REPORT', 'get reports for recurring payments'),
        ('EXTENDED_PRO_PROCESSING_REPORT', 'get reports for extended Pro processing'),
        ('EXCEPTION_PROCESSING_REPORT', 'get reports for exception processing'),
        ('ACCOUNT_MANAGEMENT_PERMISSION', 'manage your account'),
        ('INVOICING', 'manage your invoicing'),

        # These additional permissions require separate approval from PayPal
        # ('BILLING_AGREEMENT', 'obtain authorization for pre-approved payments and initiate  pre-approved transactions'),
        # ('REFERENCE_TRANSACTION', 'process a payment based on a previous transaction'),
        # ('MASS_PAY', 'initiate transactions to multiple recipients in a single batch'),
        # ('TRANSACTION_DETAILS', 'obtain transaction specific information'),
        # ('ACCOUNT_BALANCE', 'obtain your account balance'),
        # ('ENCRYPTED_WEBSITE_PAYMENTS', 'dynamically encrypt PayPal payment buttons on your web site'),
        # ('NON_REFERENCED_CREDIT', 'issue a credit to a debit or credit card'),
        # ('ACCESS_BASIC_PERSONAL_DATA', 'obtain basic attributes for specified user, such as first name, last name, and payer ID'),
        # ('ACCESS_ADVANCED_PERSONAL_DATA', 'obtain advanced attributes for specified user, such as date of birth and phone'),
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
