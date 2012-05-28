import foauth.providers


class Friendfeed(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://friendfeed.com/'
    favicon_url = 'http://friendfeed.com/favicon.ico'
    docs_url = 'http://friendfeed.com/api/documentation'

    # URLs to interact with the API
    request_token_url = 'https://friendfeed.com/account/oauth/request_token'
    authorize_url = 'https://friendfeed.com/account/oauth/authorize'
    access_token_url = 'https://friendfeed.com/account/oauth/access_token'
    api_domain = 'friendfeed-api.com'

