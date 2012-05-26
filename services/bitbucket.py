import foauth.providers


class Bitbucket(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://bitbucket.org/'
    favicon_url = 'https://dwz7u9t8u8usb.cloudfront.net/m/36a0d507acd2/img/logo_new.png'
    docs_url = 'http://confluence.atlassian.com/display/BITBUCKET/Using+the+Bitbucket+REST+APIs'

    # URLs to interact with the API
    request_token_url = 'https://bitbucket.org/api/1.0/oauth/request_token/'
    authorize_url = 'https://bitbucket.org/api/1.0/oauth/authenticate/'
    access_token_url = 'https://bitbucket.org/api/1.0/oauth/access_token/'
    api_domain = 'api.bitbucket.org'

    available_permissions = [
        (None, 'read and write your code and issues'),
    ]
