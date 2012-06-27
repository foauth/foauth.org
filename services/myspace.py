import foauth.providers


class MySpace(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.myspace.com/'
    docs_url = 'http://developerwiki.myspace.com/index.php?title=RESTful_API_Overview'

    # URLs to interact with the API
    request_token_url = 'http://api.myspace.com/request_token'
    authorize_url = 'http://api.myspace.com/authorize'
    access_token_url = 'http://api.myspace.com/access_token'
    api_domain = 'api.myspace.com'

    available_permissions = [
        (None, 'read and write your social information'),
    ]

