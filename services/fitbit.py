import foauth.providers


class FitBit(foauth.providers.Oauth1):
    # General info about the provider
    provider_url = 'http://www.fitbit.com/'
    favicon_url = 'http://www.fitbit.com/favicon.ico'
    docs_url = 'https://wiki.fitbit.com/display/API/Fitbit+API'

    # URLs to interact with the API
    request_token_url = 'http://api.fitbit.com/oauth/request_token'
    authorize_url = 'http://www.fitbit.com/oauth/authorize'
    access_token_url = 'http://api.fitbit.com/oauth/access_token'
    api_root = 'http://api.fitbit.com/'

    signature_method = foauth.providers.SIGNATURE_HMAC
    signature_location = foauth.prodivers.SIGN_HEADER

