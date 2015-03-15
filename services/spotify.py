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
        ('playlist-read-private', 'Access your private playlists'),
        ('playlist-modify-public', 'Manage your public playlists'),
        ('playlist-modify-private', 'Manage your private playlists'),
        ('streaming', 'Play music and control playback on your other devices'),
        ('user-follow-modify', 'Manage who you are following'),
        ('user-follow-read', 'Access your followers and who you are following'),
        ('user-library-read', 'Access your saved tracks and albums'),
        ('user-library-modify', 'Manage your saved tracks and albums'),
        ('user-read-private', 'Access your subscription details'),
        ('user-read-birthdate', 'Receive your birthdate'),
        ('user-read-email', 'Get your real email address'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/v1/me')
        return r.json()[u'id']
