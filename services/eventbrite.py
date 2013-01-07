from oauthlib.oauth2.draft25 import utils
import foauth.providers


class Eventbrite(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://www.eventbrite.com/'
    docs_url = 'http://developer.eventbrite.com/doc/'
    category = 'Events'

    # URLs to interact with the API
    authorize_url = 'https://www.eventbrite.com/oauth/authorize'
    access_token_url = 'https://www.eventbrite.com/oauth/token'
    api_domain = 'www.eventbrite.com'

    available_permissions = [
        (None, 'read and write to your check-ins'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/json/user_get')
        print r.content
        return unicode(r.json[u'user'][u'user_id'])
