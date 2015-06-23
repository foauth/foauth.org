from oauthlib.common import add_params_to_uri
import foauth.providers


class Jawbone(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://jawbone.com/'
    docs_url = 'https://jawbone.com/up/developer/endpoints'
    favicon_url = provider_url + 'favicon.ico'
    category = 'Fitness'

    # URLs to interact with the API
    authorize_url = 'https://jawbone.com/auth/oauth2/auth'
    access_token_url = 'https://jawbone.com/auth/oauth2/token'
    api_domain = 'jawbone.com'

    available_permissions = [
        (None, 'Read your name and profile picture'),
        ('extended_read', 'Read your age, gender, weight, and height'),
        ('location_read', "Read the places you've visited"),
        ('friends_read', 'Read your list of friends'),
        ('mood_read', 'Read your mood'),
        ('mood_write', 'Write to your mood'),
        ('move_read', 'Read your moves and workouts'),
        ('move_write', 'Write to your movies and create a workout'),
        ('sleep_read', 'Read your sleep data'),
        ('sleep_write', 'Write to your sleep data'),
        ('meal_read', 'Read your meals'),
        ('meal_write', 'Write to your meals'),
        ('weight_read', 'Read your body metrics'),
        ('weight_write', 'Write to your body metrics'),
        ('cardiac_read', 'Read your heart data'),
        ('cardiac_write', 'Write your heart data'),
        ('generic_event_read', 'Read all other types of events'),
        ('generic_event_write', 'Write to all other types of events'),
    ]

    def get_authorize_params(self, redirect_uri, scopes):
        # Always request at least user information
        scopes.append('basic_read')
        return super(Jawbone, self).get_authorize_params(redirect_uri, scopes)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/nudge/api/v.1.1/users/@me')
        return r.json()[u'data'][u'xid']
