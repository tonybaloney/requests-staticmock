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

import pytest

from six import b

from requests.compat import OrderedDict
from requests_staticmock import (Adapter,
                                 ClassAdapter,
                                 BaseMockClass,
                                 mock_session_with_fixtures,
                                 mock_session_with_class)
from requests_staticmock.responses import StaticResponseFactory
from requests import Session


def _get_session():
    session = Session()
    a = Adapter()
    session.adapters = OrderedDict()
    session.mount("http://test.com", a)
    a.register_path('tests/fixtures')
    return session


def test_session_adapter():
    response = _get_session().request('get', 'http://test.com/test.txt')
    assert response.text == 'Hello world!'


def test_json_responses():
    response = _get_session().request('get', 'http://test.com/test_json.json')
    assert response.json()['hello'] == 'world'


def test_bad_response():
    response = _get_session().request('get', 'http://test.com/bad.url')
    with pytest.raises(Exception):
        response.raise_for_status()
    assert response.status_code == 404


def test_context_manager():
    new_session = Session()
    with mock_session_with_fixtures(new_session, 'tests/fixtures',
                                    'http://test_context.com'):
        response = new_session.request('get', 'http://test_context.com/test.txt')
        assert response.text == 'Hello world!'
    # assert resets back to default 2 adapters
    assert len(new_session.adapters) == 2


def test_context_manager_multiple_urls():
    new_session = Session()
    with mock_session_with_fixtures(new_session, 'tests/fixtures',
                                    ('http://test_context.com',
                                     'http://test2_context.com')):
        response = new_session.request('get', 'http://test_context.com/test.txt')
        assert response.text == 'Hello world!'
        response2 = new_session.request('get', 'http://test2_context.com/test.txt')
        assert response2.text == 'Hello world!'
    # assert resets back to default 2 adapters
    assert len(new_session.adapters) == 2


def test_class_adapter():
    class_session = Session()
    class TestMockClass(BaseMockClass):
        def _test_json(self, request):
            return "hello alabama"

    a = ClassAdapter(TestMockClass)
    class_session.adapters = OrderedDict()
    class_session.mount("http://test.com", a)
    response = class_session.get('http://test.com/test.json')
    assert response.text == "hello alabama"


def test_class_context_manager():
    class_session = Session()
    class TestMockClass(BaseMockClass):
        def _test_json(self, request):
            return "hello alabama"

    a = ClassAdapter(TestMockClass)
    with mock_session_with_class(class_session, TestMockClass, 'http://test.com'):
        response = class_session.get('http://test.com/test.json')
    assert response.text == "hello alabama"


def test_class_context_manager_multiple_urls():
    class_session = Session()
    class TestMockClass(BaseMockClass):
        def _test_json(self, request):
            return "hello alabama"

    a = ClassAdapter(TestMockClass)
    with mock_session_with_class(class_session, TestMockClass, ('http://test.com',
                                                                'http://test2.com')):
        response = class_session.get('http://test.com/test.json')
        response2 = class_session.get('http://test2.com/test.json')
    assert response.text == "hello alabama"
    assert response2.text == "hello alabama"


def test_class_context_manager_with_params():
    class_session = Session()
    class TestMockClass(BaseMockClass):
        def _test_json(self, request):
            if request.method == 'GET':
                return 'detroit'
            else:
                return 'san diego'

    a = ClassAdapter(TestMockClass)
    with mock_session_with_class(class_session, TestMockClass, 'http://test.com'):
        response1 = class_session.get('http://test.com/test.json')
        response2 = class_session.post('http://test.com/test.json', data='123')
    assert response1.text == 'detroit'
    assert response2.text == 'san diego'


def test_class_context_manager_query():
    class_session = Session()
    class TestMockClass(BaseMockClass):
        def _test_json(self, request):
            return 'always'

    a = ClassAdapter(TestMockClass)
    with mock_session_with_class(class_session, TestMockClass, 'http://test.com'):
        response1 = class_session.get('http://test.com/test.json',
                                      params={'test': 'param'})
    assert response1.status_code == 200
    assert response1.text == 'always'


def test_class_context_manager_404_response():
    class_session = Session()
    class TestMockClass(BaseMockClass):
        def _test_json(self, request):
            return 'never'

    a = ClassAdapter(TestMockClass)
    with mock_session_with_class(class_session, TestMockClass, 'http://test.com'):
        response1 = class_session.get('http://test.com/banana.json')
    assert response1.status_code == 404


def test_class_context_manager_good_factory():
    class_session = Session()
    class TestMockClass(BaseMockClass):
        def _test_json(self, request):
            return StaticResponseFactory.GoodResponse(
                request=request,
                body=b("it's my life"),
                headers={'now': 'never'},
                status_code=201
            )

    a = ClassAdapter(TestMockClass)
    with mock_session_with_class(class_session, TestMockClass, 'http://test.com'):
        response = class_session.get('http://test.com/test.json')
    assert response.text == "it's my life"
    assert 'now' in response.headers.keys()
    assert response.headers['now'] == 'never'
    assert response.status_code == 201


def test_class_context_manager_bad_factory():
    class_session = Session()
    class TestMockClass(BaseMockClass):
        def _test_json(self, request):
            return StaticResponseFactory.BadResponse(
                request=request,
                body=b("it's not over"),
                headers={'now': 'never'},
                status_code=504
            )

    a = ClassAdapter(TestMockClass)
    with mock_session_with_class(class_session, TestMockClass, 'http://test.com'):
        response = class_session.get('http://test.com/test.json')
    assert response.text == "it's not over"
    assert 'now' in response.headers.keys()
    assert response.headers['now'] == 'never'
    assert response.status_code == 504
