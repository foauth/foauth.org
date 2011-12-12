import foauth.providers


class Digg(foauth.providers.Oauth1):
    # General info about the provider
    provider_url = 'http://digg.com/'
    favicon_url = 'http://cdn1.diggstatic.com/img/favicon.a015f25c.ico'
    docs_url = 'http://developers.digg.com/documentation'

    # URLs to interact with the API
    request_token_url = 'http://services.digg.com/oauth/request_token'
    authorize_url = 'http://digg.com/oauth/authorize'
    access_token_url = 'http://services.digg.com/oauth/access_token'
    api_root = 'http://services.digg.com/2.0/'

    signature_method = foauth.providers.SIGNATURE_HMAC
    signature_location = foauth.prodivers.SIGN_HEADER

