from oauthlib.common import add_params_to_uri
import foauth.providers


class Behance(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://www.behance.net/'
    docs_url = 'http://www.behance.net/dev/api/endpoints/'
    category = 'Career'

    # URLs to interact with the API
    authorize_url = 'https://www.behance.net/v2/oauth/authenticate'
    access_token_url = 'https://www.behance.net/v2/oauth/token'
    api_domain = 'www.behance.net'

    available_permissions = [
        (None, 'read your activity feed'),
        ('project_read', 'read your public and private projects'),
        ('post_as', 'post to your activity feed'),
        ('collection_read', 'read your private collections'),
        ('collection_write', 'write to your private collections'),
        ('invitations_read', 'read your invitations'),
        ('invitations_write', 'respond to your invitations'),
        ('wip_read', 'read your works in progress'),
        ('wip_write', 'write to your works in progress'),
    ]

    bearer_type = foauth.providers.BEARER_URI

    def get_scope_string(self, scopes):
        return '|'.join(scopes)

    def get_authorize_params(self, redirect_uri, scopes):
        # We always need to at least request something
        scopes.append('activity_read')
        return super(Behance, self).get_authorize_params(redirect_uri, scopes)

    def parse_token(self, content):
        print content
        data = super(Behance, self).parse_token(content)
        print data
        data['service_user_id'] = data['user']['id']
        return data
