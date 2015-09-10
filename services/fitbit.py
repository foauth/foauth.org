import foauth.providers


class Fitbit(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://www.fitbit.com/'
    docs_url = 'https://dev.fitbit.com/'
    category = 'Fitness'

    # URLs to interact with the API
    request_token_url = 'https://api.fitbit.com/oauth/request_token'
    authorize_url = 'https://www.fitbit.com/oauth/authorize'
    access_token_url = 'https://api.fitbit.com/oauth/access_token'
    api_domain = 'api.fitbit.com'

    available_permissions = [
        (None, 'read and write your fitness data'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/1/user/-/profile.json')
        return r.json()[u'user'][u'encodedId']
