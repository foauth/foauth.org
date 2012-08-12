import unittest
import foauth.providers
import urllib


class ProviderTests(unittest.TestCase):
    def setUp(self):
        class Example(foauth.providers.OAuth):
            provider_url = 'http://example.com'
            api_domain = 'api.example.com'

        self.provider = Example

    def test_auto_name(self):
        self.assertEqual(self.provider.name, 'Example')

    def test_auto_alias(self):
        self.assertEqual(self.provider.alias, 'example')

    def test_auto_favicon_url(self):
        primary = 'https://getfavicon.appspot.com/http://example.com'
        backup = 'https://www.google.com/s2/favicons?domain=example.com'
        url = '%s?defaulticon=%s' % (primary, urllib.quote(backup))
        self.assertEqual(self.provider.favicon_url, url)

    def test_auto_api_domains(self):
        self.assertEqual(self.provider.api_domains, ['api.example.com'])
