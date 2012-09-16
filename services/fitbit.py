import foauth.providers


class FitBit(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.fitbit.com/'
    docs_url = 'https://wiki.fitbit.com/display/API/Fitbit+API'
    category = 'Fitness'

    # URLs to interact with the API
    request_token_url = 'http://api.fitbit.com/oauth/request_token'
    authorize_url = 'http://www.fitbit.com/oauth/authorize'
    access_token_url = 'http://api.fitbit.com/oauth/access_token'
    api_domain = 'api.fitbit.com'

    available_permissions = [
        (None, 'read and write your fitness data'),
    ]
