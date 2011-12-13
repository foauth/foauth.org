import foauth.providers


class Flickr(foauth.providers.Oauth1):
    # General info about the provider
    provider_url = 'http://www.flickr.com/'
    favicon_url = 'http://l.yimg.com/g/favicon.ico'
    docs_url = 'http://www.flickr.com/services/api/'

    # URLs to interact with the API
    request_token_url = 'http://www.flickr.com/services/oauth/request_token'
    authorize_url = 'http://www.flickr.com/services/oauth/authorize'
    access_token_url = 'http://www.flickr.com/services/oauth/access_token'
    api_root = 'http://api.flickr.com/services'

    signature_method = foauth.providers.SIGNATURE_HMAC
    signature_location = foauth.prodivers.SIGN_QUERYSTRING

