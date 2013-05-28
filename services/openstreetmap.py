from xml.dom import minidom
from werkzeug.urls import url_decode

import foauth.providers


class OpenStreetMap(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'http://www.openstreetmap.org/'
    docs_url = 'http://wiki.openstreetmap.org/wiki/API'
    category = 'Mapping'

    # URLs to interact with the API
    request_token_url = 'http://www.openstreetmap.org/oauth/request_token'
    authorize_url = 'http://www.openstreetmap.org/oauth/authorize'
    access_token_url = 'http://www.openstreetmap.org/oauth/access_token'
    api_domain = 'api.openstreetmap.org'

    available_permissions = [
        (None, 'read your user preferences'),
        (None, 'modify your user preferences'),
        (None, 'created diary entries, comments and make friends'),
        (None, 'modify the map'),
        (None, 'read your private GPS traces'),
        (None, 'upload GPS traces'),
        (None, 'modify notes'),
    ]
    disclaimer = "You can select which permissions you want to authorize on the next screen, within OpenStreetMap."

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, '/api/0.6/user/details')
        dom = minidom.parseString(r.content)
        return dom.getElementsByTagName('user')[0].getAttribute('id')
