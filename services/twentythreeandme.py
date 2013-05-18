import foauth.providers

class TwentyThreeAndMe(foauth.providers.OAuth2):
    # General info about the provider
    alias = '23andme'
    name = '23andMe'
    provider_url = 'https://23andme.com/'
    docs_url = 'https://api.23andme.com/docs/'
    category = 'Genealogy'

    # URLs to interact with the API
    authorize_url = 'https://api.23andme.com/authorize/'
    access_token_url = 'https://api.23andme.com/token/'
    api_domain = 'api.23andme.com'

    available_permissions = [
        (None, 'anonymously tell whether each profile in your account is genotyped'),
        ('profile:read', 'read your profile information, including your picture'),
        ('profile:write', 'write to your profile information, including your picture'),
        ('names', 'read the full name of every profile in your account'),
        ('haplogroups', 'read your maternal and paternal haplogroups'),
        ('ancestry', 'access the full ancestral breakdown for all your profiles'),
        ('relatives', 'access your relatives who have also been genotyped'),
        ('relatives:write', 'add notes about and update relationships with relatives'),
        ('publish', 'publish shareable results so that anyone can read them'),
        ('analyses', 'access your analyzed genomes, including traits and health information'),
        ('genomes', 'read your entire genetic profile, raw and unanalyzed')
    ]

    def get_authorize_params(self, redirect_uri, scopes):
        scopes.append('basic')
        return super(TwentyThreeAndMe, self).get_authorize_params(redirect_uri, scopes)

    def get_user_id(self, key):
        r = self.api(key, self.api_domain, u'/1/user')
        return unicode(r.json()[u'id'])
