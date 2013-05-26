import requests

import foauth.providers


class FamilySearch(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://www.familysearch.com/'
    docs_url = 'https://familysearch.org/developers/docs/api/resources'
    category = 'Genealogy'

    # URLs to interact with the API
    authorize_url = 'https://sandbox.familysearch.org/cis-web/oauth2/v3/authorization'
    access_token_url = 'https://sandbox.familysearch.org/cis-web/oauth2/v3/token'
    api_domain = 'sandbox.familysearch.org'

    available_permissions = [
        (None, 'read and write to your family tree'),
    ]

    def get_access_token_response(self, redirect_uri, data):
        # Sending the (basically empty) client secret will fail,
        # so this must send its own custom request.
        return requests.post(self.get_access_token_url(), {
            'client_id': self.client_id,
            'grant_type': 'authorization_code',
            'code': data['code'],
            'redirect_uri': redirect_uri,
        }, verify=self.verify, auth=self.auth)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/platform/users/current',
                     headers={'Accept': 'application/json'})
        return unicode(r.json()[u'users'][0][u'id'])
