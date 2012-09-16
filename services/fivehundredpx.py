import foauth.providers


class FiveHundredPX(foauth.providers.OAuth1):
    # General info about the provider
    alias = '500px'
    name = '500px'
    provider_url = 'http://500px.com/'
    docs_url = 'https://github.com/500px/api-documentation'
    category = 'Pictures'

    # URLs to interact with the API
    request_token_url = 'https://api.500px.com/v1/oauth/request_token'
    authorize_url = 'https://api.500px.com/v1/oauth/authorize'
    access_token_url = 'https://api.500px.com/v1/oauth/access_token'
    api_domain = 'api.500px.com'

    available_permissions = [
        (None, 'access and manage your photos'),
    ]
