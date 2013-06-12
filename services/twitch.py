from werkzeug.urls import url_decode
import foauth.providers


class Twitch(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://twitch.tv/'
    docs_url = 'https://github.com/justintv/twitch-api'
    category = 'Videos'

    # URLs to interact with the API
    authorize_url = 'https://api.twitch.tv/kraken/oauth2/authorize'
    access_token_url = 'https://api.twitch.tv/kraken/oauth2/token'
    api_domain = 'api.twitch.tv'

    available_permissions = [
        (None, 'access your user information, including email address'),
        ('user_blocks_read', 'access your list of blocked users'),
        ('user_blocks_edit', 'block and unblock users'),
        ('user_follows_edit', 'manage your followed channels'),
        ('channel_read', "read your channel's metadata"),
        ('channel_editor', "write to your channel's metadata"),
        ('channel_commercial', 'trigger commercials on a channel'),
        ('channel_stream', "reset your channel's stream key"),
        ('channel_subscriptions', 'access all subscribers to your channel'),
        ('channel_check_subscription', 'check if specific users are subscribed to your channel'),
        ('chat_login', 'send and receive chat messages'),
    ]

    def get_authorize_params(self, redirect_uri, scopes):
        scopes.append('user_read')
        return super(Twitch, self).get_authorize_params(redirect_uri, scopes)

    def bearer_type(self, token, r):
        r.headers['Authorization'] = 'OAuth %s' % token
        return r

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/kraken/user')
        return unicode(r.json()[u'_id'])
