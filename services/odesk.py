import foauth.providers


class ODesk(foauth.providers.OAuth1):
    # General info about the provider
    name = 'oDesk'
    provider_url = 'https://www.odesk.com/'
    docs_url = 'http://developers.odesk.com/w/page/12363985/API Documentation'
    category = 'Career'

    # URLs to interact with the API
    request_token_url = 'https://www.odesk.com/api/auth/v1/oauth/token/request'
    authorize_url = 'https://www.odesk.com/services/api/auth'
    access_token_url = 'https://www.odesk.com/api/auth/v1/oauth/token/access'
    api_domain = 'www.odesk.com'

    available_permissions = [
        (None, 'access your basic info'),
        (None, 'close your contracts'),
        (None, 'create, modify and remove job posts'),
        (None, 'make a job offer'),
        (None, 'make one-time payments to your contractors'),
        (None, 'view your contracts'),
        (None, 'access your payment history'),
        (None, 'view your job posts'),
        (None, 'view your job offers'),
        (None, 'send and organize your messages'),
        (None, 'access your messages'),
        (None, 'view the structure of your companies/teams'),
        (None, 'view task codes'),
        (None, 'modify task codes'),
        (None, 'generate time and financial reports for your companies and teams'),
        (None, 'view your workdiary'),
        (None, 'modify your workdiary'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/api/auth/v1/info.json')
        return unicode(r.json()[u'auth_user'][u'uid'])
