import foauth.providers


class DeviantArt(foauth.providers.Oauth2):
    # General info about the provider
    provider_url = 'http://deviantart.com/'
    favicon_url = 'http://i.deviantart.net/icons/favicon.ico'
    docs_url = 'http://www.deviantart.com/developers/'

    # URLs to interact with the API
    authorize_url = 'https://www.deviantart.com/oauth2/draft15/authorize'
    access_token_url = 'https://www.deviantart.com/oauth2/draft15/token'
    api_root = 'https://www.deviantart.com/oauth2/draft15/'

    signature_method = foauth.providers.SIGNATURE_HMAC
    signature_location = foauth.prodivers.SIGN_HEADER

