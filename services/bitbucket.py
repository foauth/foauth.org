import foauth.providers


class BitBucket(foauth.providers.Oauth1):
    # General info about the provider
    provider_url = 'https://bitbucket.org/'
    favicon_url = 'https://dwz7u9t8u8usb.cloudfront.net/m/36a0d507acd2/img/logo_new.png'
    docs_url = 'http://confluence.atlassian.com/display/BITBUCKET/Using+the+Bitbucket+REST+APIs'

    # URLs to interact with the API
    request_token_url = 'https://bitbucket.org/api/1.0/oauth/request_token/'
    authorize_url = 'https://bitbucket.org/api/1.0/oauth/authenticate/'
    access_token_url = 'https://bitbucket.org/api/1.0/oauth/access_token/'
    api_root = 'https://api.bitbucket.org/1.0/'

    signature_method = foauth.providers.SIGNATURE_HMAC
    signature_location = foauth.prodivers.SIGN_HEADER

