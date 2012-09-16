import foauth.providers


class Friendfeed(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://friendfeed.com/'
    docs_url = 'http://friendfeed.com/api/documentation'
    category = 'Social'

    # URLs to interact with the API
    request_token_url = 'https://friendfeed.com/account/oauth/request_token'
    authorize_url = 'https://friendfeed.com/account/oauth/authorize'
    access_token_url = 'https://friendfeed.com/account/oauth/access_token'
    api_domain = 'friendfeed-api.com'

