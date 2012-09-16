from werkzeug.urls import url_decode
import foauth.providers


class Bitly(foauth.providers.OAuth2):
    # General info about the provider
    name = 'bitly'
    provider_url = 'https://bitly.com/'
    docs_url = 'https://dev.bitly.com/'
    category = 'Social'

    # URLs to interact with the API
    authorize_url = 'https://bitly.com/oauth/authorize'
    access_token_url = 'https://api-ssl.bitly.com/oauth/access_token'
    api_domain = 'api-ssl.bitly.com'

    available_permissions = [
        (None, 'read and write to your shortened URLs'),
    ]

    bearer_type = foauth.providers.BEARER_URI

    def parse_token(self, content):
        return url_decode(content)
