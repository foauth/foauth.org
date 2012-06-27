import foauth.providers


class Yahoo(foauth.providers.OAuth1):
    # General info about the provider
    name = 'Yahoo!'
    provider_url = 'http://www.yahoo.com/'
    docs_url = 'http://developer.yahoo.com/everything.html'

    # URLs to interact with the API
    request_token_url = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
    authorize_url = 'https://api.login.yahoo.com/oauth/v2/request_auth'
    access_token_url = 'https://api.login.yahoo.com/oauth/v2/get_token'
    api_domains = [
        'answers.yahooapis.com',
        'messenger.yahooapis.com',
        'social.yahooapis.com',
        'query.yahooapis.com',
        'mail.yahooapis.com',
    ]

    available_permissions = [
        (None, 'access your Yahoo! Answers private data and post content'),
        (None, 'read, write, and delete all aspects of your mail information'),
        (None, 'manage IM contacts, fetch user presence and send/receive instant messages'),
        (None, 'read and write to your contacts'),
        (None, 'read and write your profile information that is marked as public, shared with connections or private'),
        (None, 'read and write your information about social relationships to people and things'),
        (None, 'read and write your status message'),
        (None, 'read, write and delete updates information from your updates stream'),
    ]

