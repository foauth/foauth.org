import foauth.providers


class Digg(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://digg.com/'
    docs_url = 'http://developers.digg.com/documentation'
    category = 'News'

    # URLs to interact with the API
    request_token_url = 'http://services.digg.com/oauth/request_token'
    authorize_url = 'http://digg.com/oauth/authorize'
    access_token_url = 'http://services.digg.com/oauth/access_token'
    api_domain = 'services.digg.com'

    available_permissions = [
        (None, 'read and write stories and comments'),
    ]

    https = False

