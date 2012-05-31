import json
import foauth.providers


class Instagram(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://instagram.com'
    favicon_url = 'http://instagram.com/static/images/favicon.ico'
    docs_url = 'http://instagram.com/developer/'

    # URLs to interact with the API
    authorize_url = 'https://api.instagram.com/oauth/authorize/'
    access_token_url = 'https://api.instagram.com/oauth/access_token'
    api_domain = 'api.instagram.com'

    available_permissions = [
        (None, 'read all data related to you'),
        ('comments', 'create or delete comments'),
        ('relationships', 'follow and unfollow users'),
        ('likes', 'like and unlike items'),
    ]

    bearer_type = foauth.providers.BEARER_URI

    def parse_token(self, content):
        data = json.loads(content)
        return data['access_token']
