from oauthlib.common import add_params_to_uri
import foauth.providers


class Spotify(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://spotify.com/'
    docs_url = 'https://developer.spotify.com/web-api/endpoint-reference/'
    category = 'Music'

    # URLs to interact with the API
    authorize_url = 'https://accounts.spotify.com/authorize'
    access_token_url = 'https://accounts.spotify.com/api/token'
    api_domain = 'api.spotify.com'

    available_permissions = [
        (None, 'Read your publicly available information'),
        ('playlist-modify', 'Manage your public playlists'),
        ('playlist-modify-private', 'Manage all your playlists (even private)'),
        ('playlist-read-private', 'Access your private playlists'),
        ('user-read-private', 'Access your name, image and subscription details'),
        ('user-read-email', 'Get your real email address'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/v1/me')
        return r.json()[u'id']
