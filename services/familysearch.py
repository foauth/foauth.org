import foauth.providers


class FamilySearch(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'http://www.familysearch.com/'
    docs_url = 'https://familysearch.org/developers/docs/api/resources'
    category = 'Genealogy'

    # URLs to interact with the API
    authorize_url = 'https://sandbox.familysearch.org/cis-web/oauth2/v3/authorization'
    access_token_url = 'https://sandbox.familysearch.org/cis-web/oauth2/v3/token'
    api_domain = 'familygraph.myheritage.com'

    available_permissions = [
        (None, 'read and write to your family tree'),
    ]

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/platform/users/current-user',
                     headers={'Accept': 'application/json'})
        return unicode(r.json[u'id'])
