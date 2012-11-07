import foauth.providers


class Google(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://google.com/'
    docs_url = 'http://code.google.com/more/'
    category = 'Stuff'

    # URLs to interact with the API
    authorize_url = 'https://accounts.google.com/o/oauth2/auth'
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    api_domains = [
        'www.googleapis.com',
        'www.blogger.com',
        'docs.google.com',
        'www.google.com',
        # TODO: Find more and add them here
    ]

    bearer_type = foauth.providers.BEARER_URI

    # Scopes: https://code.google.com/oauthplayground/
    # Also, search for "site:code.google.com https://www.googleapis.com/auth/"
    available_permissions = [
        ('https://www.googleapis.com/auth/userinfo.email', 'read your email address'),
        ('https://www.googleapis.com/auth/userinfo.profile', 'read your basic profile information'),
        ('https://www.googleapis.com/auth/analytics', 'access your analytics'),
        ('https://www.googleapis.com/auth/blogger', 'access your blogs'),
        ('https://www.googleapis.com/auth/books', 'access your books'),
        ('https://www.googleapis.com/auth/calendar', 'access your calendars'),
        ('https://www.googleapis.com/auth/contacts', 'access your contacts'),
        ('https://www.googleapis.com/auth/structuredcontent', 'access shopping data'),
        ('https://www.googleapis.com/auth/docs', 'access your documents'),
        ('https://www.googleapis.com/auth/picasa', 'access your photos'),
        ('https://www.googleapis.com/auth/spreadsheets', 'access your spreadsheets'),
        ('https://www.googleapis.com/auth/tasks', 'read and write to your tasks'),
        ('https://www.googleapis.com/auth/plus.me', 'access your Google+ data'),
        ('https://www.googleapis.com/auth/urlshortener', 'access your shortened URLs'),
        ('https://www.googleapis.com/auth/youtube', 'access your videos'),
        ('https://www.googleapis.com/auth/adsense', 'manage your adsense data'),
        ('https://www.googleapis.com/auth/gan', 'manage your affiliate options'),
        ('https://www.googleapis.com/auth/devstorage.read_write', 'read and write to your cloud storage'),
        ('https://www.googleapis.com/auth/structuredcontent', 'access shopping content'),
        ('https://www.googleapis.com/auth/chromewebstore', 'access your Chrome store settings'),
        ('https://www.googleapis.com/auth/drive.file', 'access your Google Drive'),
        ('https://www.googleapis.com/auth/latitude.all.best', 'access your location information'),
        ('https://www.googleapis.com/auth/moderator', 'access moderator content'),
        ('https://www.googleapis.com/auth/orkut', 'access your Orkut data'),
        ('https://www.googleapis.com/auth/youtube', 'access your videos'),

        ('http://www.google.com/reader/api', 'access your news feeds'),
        ('http://www.google.com/webmasters/tools/feeds/', 'access your webmaster tools'),
        ('http://finance.google.com/finance/feeds/', 'access financial information'),
        ('https://mail.google.com/', 'access your email'),
        ('http://maps.google.com/maps/feeds/', 'access your custom maps'),
        ('https://sites.google.com/feeds/', 'access your sites'),

        # TODO: Find more and add them here
    ]

    def get_authorize_params(self, *args, **kwargs):
        params = super(Google, self).get_authorize_params(*args, **kwargs)
        params['access_type'] = 'offline'
        return params

    def get_user_id(self, key):
        r = self.api(key, self.api_domains[0], u'/oauth2/v2/userinfo')
        return r.json[u'id']
