import foauth.providers


class Dailymotion(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://www.dailymotion.com/'
    docs_url = 'http://www.dailymotion.com/doc/api/graph-api.html'
    category = 'Videos'

    # URLs to interact with the API
    authorize_url = 'https://api.dailymotion.com/oauth/authorize'
    access_token_url = 'https://api.dailymotion.com/oauth/token'
    api_domain = 'api.dailymotion.com'

    available_permissions = [
        (None, 'access your public profile information'),
        ('email', 'access your email address'),
        ('userinfo', 'read and write to your private profile information'),
        ('manage_videos', 'publish, modify and delete your videos'),
        ('manage_comments', 'publish comments on videos'),
        ('manage_playlists', 'create, edit and delete your playlists'),
        ('manage_tiles', 'read and write to your saved tiles'),
        ('manage_subscriptions', 'manage your subscriptions'),
        ('manage_friends', 'manage your list of friends'),
        ('manage_favorites', 'manage your list of favorite videos'),
        ('manage_groups', 'manage your groups'),
    ]

    available_permissions = [
        (None, 'access your personal assets'),
        ('email', 'access your email'),
        ('userinfo', 'access ane edit your personal information'),
        ('manage_videos', 'access and edit your videos'),
        ('manage_comments', 'access and edit your comments'),
        ('manage_playlists', 'access and edit your playlists'),
        ('manage_tiles', 'access and edit your dashboard'),
        ('manage_subscriptions', 'access and edit your following tab'),
        ('manage_friends', 'access and edit your friends'),
        ('manage_favorites', 'access and edit your favorites'),
        ('manage_groups', 'access and edit your groups'),
    ]

    def bearer_type(self, token, r):
        r.headers['Authorization'] = 'OAuth %s' % token
        return r

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/me')
        return unicode(r.json()[u'id'])
