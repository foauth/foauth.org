import foauth.providers
import urlparse


class Evernote(foauth.providers.OAuth1):
    # General info about the provider
    provider_url = 'https://www.evernote.com/'
    docs_url = 'https://www.evernote.com/about/developer/api/'

    # URLs to interact with the API
    request_token_url = 'https://www.evernote.com/oauth'
    authorize_url = 'https://www.evernote.com/OAuth.action'
    access_token_url = 'https://www.evernote.com/oauth'
    api_domain = 'www.evernote.com'

    def get_access_token(self):
        # Override standard token request to also get the data shard
        data = super(Evernote, self).get_access_token()
        self.shard = data['edam_shard']
        return data

    def get_api_root(self):
        # Override standard API root to add the data shard
        return urlparse.urljoin(self.api_root, self.shard + '/')

