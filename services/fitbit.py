import requests

import foauth.providers


class Fitbit(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://www.fitbit.com/'
    docs_url = 'https://dev.fitbit.com/'
    category = 'Fitness'

    # URLs to interact with the API
    authorize_url = 'https://www.fitbit.com/oauth2/authorize'
    access_token_url = 'https://api.fitbit.com/oauth2/token'
    api_domain = 'api.fitbit.com'

    available_permissions = [
        (None, 'read and write your user profile'),
        ('activity', 'read and write your activity data'),
        ('heartrate', 'read and write your heart rate'),
        ('location', 'read and write your location'),
        ('nutrition', 'read and write your nutrition information'),
        ('settings', 'manage your account and device settings'),
        ('sleep', 'read and write to your sleep logs'),
        ('social', 'manage your friends'),
        ('weight', 'read and write your weight information'),
    ]

    def __init__(self, *args, **kwargs):
        super(Fitbit, self).__init__(*args, **kwargs)
        self.auth = (self.client_id, self.client_secret)

    def get_authorize_params(self, redirect_uri, scopes):
        # Always request profile info, in order to get the user ID
        scopes.append('profile')
        return super(Fitbit, self).get_authorize_params(redirect_uri, scopes)

    def get_access_token_response(self, redirect_uri, data):
        # Need a custom request here in order to include state
        return requests.post(self.get_access_token_url(), {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': data['code'],
            'redirect_uri': redirect_uri,
            'state': data['state'],
        }, verify=self.verify, auth=self.auth)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/1/user/-/profile.json')
        return r.json()[u'user'][u'encodedId']
