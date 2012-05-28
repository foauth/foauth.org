import foauth.providers


class GetSatisfaction(foauth.providers.OAuth1):
    # General info about the provider
    name = 'Get Satisfaction'
    provider_url = 'http://getsatisfaction.com/'
    favicon_url = 'http://getsatisfaction.com/sites/default/files/getsatisfaction_favicon_0.ico'
    docs_url = 'http://getsatisfaction.com/developers/api-resources'

    # URLs to interact with the API
    request_token_url = 'http://getsatisfaction.com/api/request_token'
    authorize_url = 'http://getsatisfaction.com/api/authorize'
    access_token_url = 'http://getsatisfaction.com/api/access_token'
    api_domain = 'api.getsatisfaction.com'

