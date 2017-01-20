#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_requests_staticmock
----------------------------------

Tests for `requests_staticmock` module.
"""

import unittest

from requests_staticmock import adapter
from requests import Session


class TestRequestsStaticMock(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_session_adapter(self):
        s = Session()
        a = adapter.Adapter()
        s.mount("http://test.com", a)
        a.register_path('tests/fixtures')
        
        response = s.request('get', 'http://test.com/test.txt')
        self.assertEqual(response.text, 'Hello world!')


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
