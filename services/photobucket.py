import foauth.providers
from oauthlib.oauth1.rfc5849 import SIGNATURE_TYPE_QUERY


class Photobucket(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.photobucket.com/'
    docs_url = 'http://pic.pbsrc.com/dev_help/WebHelpPublic/PhotobucketPublicHelp.htm'
    category = 'Pictures'

    # URLs to interact with the API
    request_token_url = 'http://api.photobucket.com/login/request'
    authorize_url = 'http://photobucket.com/apilogin/login'
    access_token_url = 'http://api.photobucket.com/login/access'
    api_domain = 'api.photobucket.com'

    available_permissions = [
        (None, 'read and manage your pictures'),
    ]

    https = False
    signature_type = SIGNATURE_TYPE_QUERY

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/user', params={'format': 'json'})
        return r.json[u'content'][u'username']
