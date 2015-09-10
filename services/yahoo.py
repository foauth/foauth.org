from xml.dom import minidom

import foauth.providers


class Yahoo(foauth.providers.OAuth1):
    # General info about the provider
    name = 'Yahoo!'
    provider_url = 'https://www.yahoo.com/'
    docs_url = 'https://developer.yahoo.com/everything.html'
    favicon_url = provider_url + 'favicon.ico'
    category = 'Productivity'

    # URLs to interact with the API
    request_token_url = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
    authorize_url = 'https://api.login.yahoo.com/oauth/v2/request_auth'
    access_token_url = 'https://api.login.yahoo.com/oauth/v2/get_token'
    api_domains = [
        'social.yahooapis.com',
        'answers.yahooapis.com',
        'messenger.yahooapis.com',
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

    https = False

    def get_user_id(self, key):
        r = self.api(key, self.api_domains[0], u'/v1/me/guid')
        dom = minidom.parseString(r.content)
        return dom.getElementsByTagName('value')[0].firstChild.nodeValue
