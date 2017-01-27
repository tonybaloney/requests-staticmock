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

from requests.adapters import BaseAdapter, HTTPAdapter
from requests_staticmock.responses import StaticResponseFactory


BASE_PATH = os.getcwd()


class Adapter(BaseAdapter):
    def __init__(self):
        self.paths = []
        self._http_adapter = HTTPAdapter()

    def send(self, request, **kwargs):
        path_url = request.path_url
        match = None
        for path in self.paths:
            target_path = os.path.normpath(os.path.join(BASE_PATH,
                                                        path,
                                                        path_url[1:]))
            if os.path.isfile(target_path):
                match = target_path
                break
        if match:
            with open(match, 'r') as fo:
                body = fo.read()
            return StaticResponseFactory.GoodResponse(body=body,
                                                      request=request)
        else:
            return StaticResponseFactory.BadResponse(status_code=404,
                                                     request=request,
                                                     body="Not found.")

    def close(self):
        pass

    def register_path(self, path):
        self.paths.append(path)
