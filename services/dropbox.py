import foauth.providers


class Dropbox(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://www.dropbox.com/'
    docs_url = 'https://www.dropbox.com/developers/reference/api'
    favicon_url = 'https://cf.dropboxstatic.com/static/images/favicon-vflk5FiAC.ico'
    category = 'Files'

    # URLs to interact with the API
    authorize_url = 'https://www.dropbox.com/oauth2/authorize'
    access_token_url = 'https://api.dropboxapi.com/oauth2/token'
    api_domains = ['api.dropboxapi.com', 'content.dropboxapi.com', 'notify.dropboxapi.com']

    available_permissions = [
        (None, 'read and write to your entire Dropbox'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domains[0], u'/2/users/get_current_account', method='POST')
        return unicode(r.json()[u'account_id'])
