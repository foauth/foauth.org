import foauth.providers


class Meetup(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://www.meetup.com/'
    docs_url = 'http://www.meetup.com/meetup_api/'

    # URLs to interact with the API
    authorize_url = 'https://secure.meetup.com/oauth2/authorize'
    access_token_url = 'https://secure.meetup.com/oauth2/access'
    api_domain = 'api.meetup.com'

    bearer_type = foauth.providers.BEARER_URI

    available_permissions = [
        (None, 'access your groups, create and edit events, and post photos'),
        ('messaging', 'send and receive messages'),
        ('ageless', 'keep the authorization active for two weeks'),
    ]

