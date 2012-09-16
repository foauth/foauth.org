import foauth.providers


class Ohloh(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://www.ohloh.net/'
    docs_url = 'http://meta.ohloh.net/reference/'
    category = 'Code'

    # URLs to interact with the API
    request_token_url = 'http://www.ohloh.net/oauth/request_token'
    authorize_url = 'http://www.ohloh.net/oauth/authorize'
    access_token_url = 'http://www.ohloh.net/oauth/access_token'
    api_domain = 'www.ohloh.net'

    available_permissions = [
        (None, 'read and write to your software usage'),
    ]
