import foauth.providers


class Dropbox(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://www.dropbox.com/'
    favicon_url = 'https://www.dropbox.com/static/20659/images/favicon.ico'
    docs_url = 'https://www.dropbox.com/developers/reference/api'

    # URLs to interact with the API
    request_token_url = 'https://api.dropbox.com/1/oauth/request_token'
    authorize_url = 'https://www.dropbox.com/1/oauth/authorize'
    access_token_url = 'https://api.dropbox.com/1/oauth/access_token'
    api_domains = ['api.dropbox.com', 'api-content.dropbox.com']

    available_permissions = [
        (None, 'read and write to your entire Dropbox'),
    ]

