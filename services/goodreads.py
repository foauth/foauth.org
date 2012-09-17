import foauth.providers
from xml.dom import minidom


class Goodreads(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.goodreads.com/'
    docs_url = 'http://www.goodreads.com/api'
    category = 'Books'

    # URLs to interact with the API
    request_token_url = 'http://www.goodreads.com/oauth/request_token'
    authorize_url = 'http://www.goodreads.com/oauth/authorize'
    access_token_url = 'http://www.goodreads.com/oauth/access_token'
    api_domain = 'www.goodreads.com'

    https = False

    available_permissions = [
        (None, 'read and write to your reading history'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/api/auth_user')
        dom = minidom.parseString(r.content)
        return dom.getElementsByTagName('user')[0].getAttribute('id')
