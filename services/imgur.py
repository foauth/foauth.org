import foauth.providers


class Imgur(foauth.providers.OAuth1):
    # General info about the provider
    name = 'imgur'
    provider_url = 'http://imgur.com/'
    docs_url = 'http://api.imgur.com/'
    category = 'Pictures'

    # URLs to interact with the API
    request_token_url = 'https://api.imgur.com/oauth/request_token'
    authorize_url = 'https://api.imgur.com/oauth/authorize'
    access_token_url = 'https://api.imgur.com/oauth/access_token'
    api_domain = 'api.imgur.com'

    available_permissions = [
        (None, 'read and write to your images'),
    ]
