from oauthlib.oauth2.draft25 import utils
import foauth.providers


class Dwolla(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://dwolla.com/'
    docs_url = 'http://developers.dwolla.com/dev/docs'
    category = 'Money'

    # Required by Dwolla's ToS
    disclaimer = "This application is not directly supported by Dwolla Corp. Dwolla Corp. makes no claims about this application.  This application is not endorsed or certified by Dwolla Corp."

    # URLs to interact with the API
    authorize_url = 'https://www.dwolla.com/oauth/v2/authenticate'
    access_token_url = 'https://www.dwolla.com/oauth/v2/token'
    api_domain = 'www.dwolla.com'

    available_permissions = [
        (None, 'access your account details'),
        ('Contacts', 'read your contacts'),
        ('Transactions', 'read your transaction history'),
        ('Balance', 'read your current balance'),
        ('Send', 'send money to others'),
        ('Request', 'request money from others'),
        ('Funding', 'view your bank accounts and other funding sources'),
    ]

    def bearer_type(self, token, r):
        r.url = utils.add_params_to_uri(r.url, [((u'oauth_token', token))])
        return r

    def get_authorize_params(self, redirect_uri, scopes):
        # Always request account info, in order to get the user ID
        scopes.append('AccountInfoFull')
        return super(Dwolla, self).get_authorize_params(redirect_uri, scopes)

    def get_scope_string(self, scopes):
        # Dwolla doesn't follow the spec on this point
        return '|'.join(scopes)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/oauth/rest/users/')
        return unicode(r.json[u'Response'][u'Id'])
