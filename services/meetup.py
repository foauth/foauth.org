import datetime
import json

import foauth


class Meetup(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://www.meetup.com/'
    favicon_url = 'http://www.meetup.com/favicon.ico'
    docs_url = 'http://www.meetup.com/meetup_api/'

    # URLs to interact with the API
    authorize_url = 'https://secure.meetup.com/oauth2/authorize'
    access_token_url = 'https://secure.meetup.com/oauth2/access'
    api_domain = 'http://api.meetup.com/'

    available_permissions = [
        (None, 'access your groups, create and edit events, and post photos'),
        ('messaging', 'send and receive messages'),
        ('ageless', 'keep the authorization active for two weeks'),
    ]

    def parse_token(self, content):
        data = json.loads(content)
        expires = data.get('expires_in', None)
        if expires:
            expires = datetime.datetime.now() + datetime.timedelta(seconds=expires)
        return data['access_token'], expires
