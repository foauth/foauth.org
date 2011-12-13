import foauth


class Foursquare(foauth.providers.Oauth2):
    # General info about the provider
    provider_url = 'http://www.foursquare.com/'
    favicon_url = 'https://static-s.foursquare.com/favicon-c62b82f6120e2c592a3e6f3476d66554.ico'
    docs_url = 'https://developer.foursquare.com/overview/'

    # URLs to interact with the API
    authorize_url = 'https://foursquare.com/oauth2/authorize'
    access_token_url = 'https://foursquare.com/oauth2/access_token'
    api_root = 'https://api.foursquare.com/v2/'

    signature_method = foauth.providers.SIGNATURE_HMAC
    signature_location = foauth.prodivers.SIGN_HEADER


