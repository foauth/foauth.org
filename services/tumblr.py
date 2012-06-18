import foauth.providers


class Tumblr(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.tumblr.com/'
    favicon_url = 'http://assets.tumblr.com/images/favicon.gif'
    docs_url = 'http://www.tumblr.com/docs/en/api/v2'

    # URLs to interact with the API
    request_token_url = 'http://www.tumblr.com/oauth/request_token'
    authorize_url = 'http://www.tumblr.com/oauth/authorize'
    access_token_url = 'http://www.tumblr.com/oauth/access_token'
    api_domain = 'api.tumblr.com'

    https = False

    available_permissions = [
        (None, 'read, write and manage your blog'),
    ]

