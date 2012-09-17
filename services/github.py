from werkzeug.urls import url_decode
import foauth.providers


class GitHub(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://github.com/'
    docs_url = 'http://developer.github.com/v3/'
    category = 'Code'

    # URLs to interact with the API
    authorize_url = 'https://github.com/login/oauth/authorize'
    access_token_url = 'https://github.com/login/oauth/access_token'
    api_domain = 'api.github.com'

    available_permissions = [
        (None, 'read your public profile, public repo info and gists'),
        ('user', 'write to your profile'),
        ('public_repo', 'write to your public repo info'),
        ('repo', 'write to your public and private repo info'),
        ('gist', 'write to your gists'),
    ]

    supports_state = False

    def get_scope_string(self, scopes):
        # GitHub doesn't follow the spec on this point
        return ','.join(scopes)

    def parse_token(self, content):
        return url_decode(content)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/user')
        return unicode(r.json[u'id'])
