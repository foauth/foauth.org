import flask
import foauth.providers


class GetGlue(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://getglue.com/'
    favicon_url = 'http://getglue.com/favicon.ico'
    docs_url = 'http://getglue.com/api'

    # URLs to interact with the API
    request_token_url = 'https://api.getglue.com/oauth/request_token'
    authorize_url = 'http://getglue.com/oauth/authorize'
    access_token_url = 'https://api.getglue.com/oauth/access_token'
    api_domain = 'api.getglue.com'

    available_permissions = [
        (None, 'read and write your social checkins'),
    ]

    def get_authorize_params(self):
        # GetGlue doesn't parrot this back, so we have to save it
        params = super(GetGlue, self).get_authorize_params()
        flask.session['%s_temp_token' % self.alias] = params['oauth_token']
        return params

    def callback(self, data):
        # GetGlue doesn't parrot this back, so we have to retrieve it
        data = dict(data, oauth_token=flask.session['%s_temp_token' % self.alias])
        del flask.session['%s_temp_token' % self.alias]
        return super(GetGlue, self).callback(data)

