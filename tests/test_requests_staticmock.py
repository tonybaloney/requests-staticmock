#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_requests_staticmock
----------------------------------

Tests for `requests_staticmock` module.
"""

import unittest
from collections import OrderedDict

from requests_staticmock import adapter
from requests import Session


class TestRequestsStaticMock(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        a = adapter.Adapter()
        self.session.adapters = OrderedDict()
        self.session.mount("http://test.com", a)
        a.register_path('tests/fixtures')

    def tearDown(self):
        pass

    def test_session_adapter(self):
        response = self.session.request('get', 'http://test.com/test.txt')
        self.assertEqual(response.text, 'Hello world!')

    def test_json_responses(self):
        response = self.session.request('get', 'http://test.com/test_json.json')
        self.assertEqual(response.json()['hello'], 'world')

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
