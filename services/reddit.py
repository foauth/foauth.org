from oauthlib.oauth2.draft25 import utils
import foauth.providers


class Reddit(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://www.reddit.com/'
    docs_url = 'http://www.reddit.com/dev/api'
    category = 'News'

    # URLs to interact with the API
    authorize_url = 'https://ssl.reddit.com/api/v1/authorize'
    access_token_url = 'https://ssl.reddit.com/api/v1/access_token'
    api_domain = 'oauth.reddit.com'

    available_permissions = [
        (None, 'access your identity information'),
        ('read', 'read information about articles'),
        ('vote', 'vote on articles'),
        ('submit', 'submit new articles and comments'),
        ('edit', 'edit your posts and comments'),
        ('mysubreddits', 'manage your subreddits'),
        ('subscribe', 'manage your subscriptions'),
        ('modlog', 'view your moderation logs'),
        ('modposts', 'moderate posts in your subreddits'),
        ('modflair', 'manage and assign flair in your subreddits'),
        ('modconfig', 'manage the configuration of your subreddits'),
        ('privatemessages', 'read and write to your private messages'),
    ]

    def get_authorize_params(self, redirect_uri, scopes):
        # Always request account info, in order to get the user ID
        scopes.append('identity')
        params = super(Reddit, self).get_authorize_params(redirect_uri, scopes)
        # Make sure we get refresh tokens
        params['duration'] = 'permanent'
        return params

    def get_scope_string(self, scopes):
        return ','.join(scopes)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/api/v1/me')
        print 'User Content: %r' % r.content
        return unicode(r.json[u'id'])
