import foauth.providers


class Wordpress(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://www.wordpress.com/'
    docs_url = 'http://developer.wordpress.com/docs/api/'

    # URLs to interact with the API
    authorize_url = 'https://public-api.wordpress.com/oauth2/authorize'
    access_token_url = 'https://public-api.wordpress.com/oauth2/token'
    api_domain = 'public-api.wordpress.com'

    available_permissions = [
        (None, 'read and post to your blog'),
    ]

