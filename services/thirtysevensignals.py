import foauth.providers


class ThirtySevenSignals(foauth.providers.OAuth2):
    # General info about the provider
    alias = '37signals'
    name = '37signals'
    provider_url = 'https://37signals.com/'
    docs_url = 'https://github.com/37signals/api'
    category = 'Productivity'

    # URLs to interact with the API
    authorize_url = 'https://launchpad.37signals.com/authorization/new?type=web_server'
    access_token_url = 'https://launchpad.37signals.com/authorization/token?type=web_server'
    api_domains = [
        'launchpad.37signals.com',
        'basecamp.com',
        'campfire.com',
        'highrisehq.com',
    ]

    available_permissions = [
        (None, 'access your information'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domains[0], u'/authorization.json')
        return unicode(r.json[u'identity'][u'id'])
