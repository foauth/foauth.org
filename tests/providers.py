import unittest
import foauth.providers


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
        url = 'https://www.google.com/s2/favicons?domain=example.com'
        self.assertEqual(self.provider.favicon_url, url)

    def test_auto_api_domains(self):
        self.assertEqual(self.provider.api_domains, ['api.example.com'])
