# -*- coding: utf-8 -*-
# Licensed to Anthony Shaw (anthonyshaw@apache.org) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from requests.compat import OrderedDict
from requests_staticmock import (Adapter,
                                 mock_session_with_fixtures)
from requests import Session


class TestRequestsStaticMock(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        a = Adapter()
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

    def test_bad_response(self):
        response = self.session.request('get', 'http://test.com/bad.url')
        with self.assertRaises(Exception):
            response.raise_for_status()
        self.assertEquals(response.status_code, 404)

    def test_context_manager(self):
        new_session = Session()
        with mock_session_with_fixtures(new_session, 'tests/fixtures',
                                        'http://test_context.com'):
            response = new_session.request('get', 'http://test_context.com/test.txt')
            self.assertEqual(response.text, 'Hello world!')
        # assert resets back to default 2 adapters
        self.assertEqual(len(new_session.adapters), 2)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
