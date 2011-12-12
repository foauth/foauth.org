import foauth


class Dropbox(foauth.providers.Oauth1):
    # General info about the provider
    provider_url = 'https://www.dropbox.com/'
    favicon_url = 'https://www.dropbox.com/static/20659/images/favicon.ico'
    docs_url = 'https://www.dropbox.com/developers/reference/api'

    # URLs to interact with the API
    request_token_url = 'https://api.dropbox.com/1/oauth/request_token'
    authorize_url = 'https://www.dropbox.com/1/oauth/authorize'
    access_token_url = 'https://api.dropbox.com/1/oauth/access_token'
    api_root = 'https://api.dropbox.com/1/'

    signature_method = foauth.providers.SIGNATURE_HMAC
    signature_location = foauth.prodivers.SIGN_HEADER

