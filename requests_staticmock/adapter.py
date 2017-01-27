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

import os.path
import os
import six
from six import b

from requests.adapters import BaseAdapter
from requests_staticmock.responses import StaticResponseFactory
from requests_staticmock.abstractions import BaseMockClass

__all__ = [
    'Adapter',
    'ClassAdapter'
]

BASE_PATH = os.getcwd()


class Adapter(BaseAdapter):
    def __init__(self, base_path=None):
        self.paths = []
        if base_path:
            self.register_path(base_path)

    def match_url(self, request):
        path_url = request.path_url
        match = None
        for path in self.paths:
            target_path = os.path.normpath(os.path.join(BASE_PATH,
                                                        path,
                                                        path_url[1:]))
            if os.path.isfile(target_path):
                match = target_path
                break
        return match

    def response_from_fixture(self, request, fixture_path):
        with open(fixture_path, 'rb') as fo:
                body = fo.read()
        return StaticResponseFactory.GoodResponse(body=body,
                                                  request=request)

    def send(self, request, **kwargs):
        match = self.match_url(request)
        if match:
            return self.response_from_fixture(request=request,
                                              fixture_path=match)
        else:
            return StaticResponseFactory.BadResponse(status_code=404,
                                                     request=request,
                                                     body=b("Not found."))

    def close(self):
        pass

    def register_path(self, path):
        self.paths.append(path)


class ClassAdapter(Adapter):
    def __init__(self, cls):
        if not issubclass(cls, BaseMockClass):
            raise TypeError("Must be BaseMockClass")

        cls = cls()
        self.cls = cls

    def send(self, request, **kwargs):
        method_name = request.path_url.replace('/', '_').replace('.', '_')
        if '?' in method_name:
            method_name = method_name.split('?')[0]
        if hasattr(self.cls, method_name):
            match = getattr(self.cls, method_name)
            response = match(request)
            if isinstance(response, six.string_types):
                return StaticResponseFactory.GoodResponse(
                    body=b(response),
                    request=request)
            else:
                return response
        else:
            return StaticResponseFactory.BadResponse(status_code=404,
                                                     request=request,
                                                     body=b("Not found."))
