import flask
import foauth.providers


class GetGlue(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://getglue.com/'
    docs_url = 'http://getglue.com/api'
    category = 'Entertainment'

    # URLs to interact with the API
    request_token_url = 'https://api.getglue.com/oauth/request_token'
    authorize_url = 'http://getglue.com/oauth/authorize'
    access_token_url = 'https://api.getglue.com/oauth/access_token'
    api_domain = 'api.getglue.com'

    available_permissions = [
        (None, 'read and write your social checkins'),
    ]

    def get_authorize_params(self, redirect_uri):
        # GetGlue doesn't parrot this back, so we have to save it
        params = super(GetGlue, self).get_authorize_params(redirect_uri)
        flask.session['%s_temp_token' % self.alias] = params['oauth_token']
        return params

    def callback(self, data, *args, **kwargs):
        # GetGlue doesn't parrot this back, so we have to retrieve it
        data = dict(data, oauth_token=flask.session['%s_temp_token' % self.alias])
        del flask.session['%s_temp_token' % self.alias]
        return super(GetGlue, self).callback(data, *args, **kwargs)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/v2/user/profile?format=json')
        return r.json[u'profile'][u'username']
