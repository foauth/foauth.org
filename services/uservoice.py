import foauth.providers


class UserVoice(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://uservoice.com/'
    favicon_url = 'http://uservoice.com/favicon.ico'
    docs_url = 'http://developer.uservoice.com/docs/api/reference/'

    # URLs to interact with the API
    request_token_url = 'http://uservoice.com/api/v1/oauth/access_token'
    authorize_url = 'http://uservoice.com/api/v1/oauth/authorize'
    access_token_url = 'http://uservoice.com/api/v1/oauth/request_token'
    api_domain = 'uservoice.com'

