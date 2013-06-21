import foauth.providers
from foauth import OAuthDenied


class Elance(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://www.elance.com/'
    docs_url = 'https://www.elance.com/q/api2'
    category = 'Career'

    # URLs to interact with the API
    authorize_url = 'https://api.elance.com/api2/oauth/authorize'
    access_token_url = 'https://api.elance.com/api2/oauth/token'
    api_domain = 'api.elance.com'

    available_permissions = [
        (None, 'access and manage your Elance account'),
    ]

    bearer_type = foauth.providers.BEARER_URI

    def parse_token(self, content):
        return super(Elance, self).parse_token(content)[u'data']

    def callback(self, data, *args, **kwargs):
        if data.get('error') == 'access_denied':
            raise OAuthDenied('Denied access to Elance')

        return super(Elance, self).callback(data, *args, **kwargs)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/api2/profiles/my')
        return unicode(r.json()[u'data'][u'providerProfile'][u'userId'])
