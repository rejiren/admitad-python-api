import unittest
from mocker import MockerTestCase
from pyadmitad.api import get_oauth_client
from pyadmitad.constants import *
from pyadmitad.transport import prepare_api_url, build_headers,\
    HttpTransportPagination


class WebsiteTypesTestCase(MockerTestCase):

    def set_mocker(self, limit=None, offset=None):
        access_token = 'access_token'
        self.client = get_oauth_client(access_token)
        obj = self.mocker.patch(self.client.transport)
        url = prepare_api_url(WEBSITE_TYPES_URL)
        kwargs = {
            'data': HttpTransportPagination(
                limit=limit, offset=offset).to_value(),
            'headers': build_headers(access_token),
            'method': 'GET'
        }
        obj.api_request(url, **kwargs)

    def test_website_types_request(self):
        self.set_mocker()
        result = {
            u'results': [
                u'website',
                u'doorway',
                u'contextual',
                u'social_app',
                u'social_group',
                u'social_teaser',
                u'arbitrage'
            ],
            u'_meta': {
                u'count': 7,
                u'limit': 20,
                u'offset': 0
            }
        }
        self.mocker.result(result)
        self.mocker.replay()
        res = self.client.WebsiteTypes.getAll()
        self.assertIn(u'results', res)
        self.assertIn(u'_meta', res)
        self.assertIsInstance(res[u'results'], list)
        self.mocker.verify()

    def test_website_types_request_with_pagination(self):
        self.set_mocker(offset=1, limit=2)
        result = {
            u'results': [
                u'doorway',
                u'contextual'
            ],
            u'_meta': {
                u'count': 7,
                u'limit': 2,
                u'offset': 1
            }
        }
        self.mocker.result(result)
        self.mocker.replay()
        res = self.client.WebsiteTypes.getAll(offset=1, limit=2)
        self.assertIn(u'results', res)
        self.assertIn(u'_meta', res)
        self.assertIsInstance(res[u'results'], list)
        self.assertEqual(len(res[u'results']), 2)
        _meta = res[u'_meta']
        self.assertEqual(_meta[u'count'], 7)
        self.assertEqual(_meta[u'limit'], 2)
        self.assertEqual(_meta[u'offset'], 1)
        self.mocker.verify()


if __name__ == '__main__':
    unittest.main()
