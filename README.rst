===============================
requests-staticmock
===============================

.. image:: https://img.shields.io/pypi/v/requests-staticmock.svg
        :target: https://pypi.python.org/pypi/requests-staticmock

.. image:: https://img.shields.io/travis/tonybaloney/requests-staticmock.svg
        :target: https://travis-ci.org/tonybaloney/requests-staticmock

.. image:: https://readthedocs.org/projects/requests-staticmock/badge/?version=latest
        :target: https://readthedocs.org/projects/requests-staticmock/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/tonybaloney/requests-staticmock/badge.svg?branch=master
        :target: https://coveralls.io/github/tonybaloney/requests-staticmock?branch=master

.. image:: https://pyup.io/repos/github/tonybaloney/requests-staticmock/shield.svg
     :target: https://pyup.io/repos/github/tonybaloney/requests-staticmock/
     :alt: Updates

.. image:: https://pyup.io/repos/github/tonybaloney/requests-staticmock/python-3-shield.svg
     :target: https://pyup.io/repos/github/tonybaloney/requests-staticmock/
     :alt: Python 3

A static HTTP mock interface for testing classes that leverage Python `requests` with **no** monkey patching!

* Free software: Apache 2 License
* Documentation: https://requests-staticmock.readthedocs.org.

Usage
-----

As a context manager for requests Session instances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: requests_staticmock.context
    :members: mock_session_with_fixtures

Example
+++++++

.. code-block:: python

    import requests
    import requests_staticmock
    
    session = requests.Session()
    with requests_staticmock.mock_session_with_fixtures(session, 'tests/fixtures', 'http://test_context.com'):
        # will return a response object with the contents of tests/fixtures/test.json
        response = new_session.request('get', 'http://test_context.com/test.json')

As an adapter
~~~~~~~~~~~~~

You can inject the `requests_staticmock` adapter into an existing (or new) requests session to mock out a particular URL
or domain, e.g.

.. code-block:: python

    import requests
    from requests_staticmock import Adapter
    
    session = requests.Session()
    special_adapter = Adapter('fixtures')
    session.mount('http://specialwebsite.com', special_adapter)
    session.request('http://normal.com/api/example') # works as normal
    session.request('http://specialwebsite.com') # returns static mocks

Class adapter
~~~~~~~~~~~~~

Instead of using a static asset adapter, you can use an adapter that expects an internal method to respond with a string, e.g.

GET `/test/example.xml` will call method `_test_example_xml(self, request)`

GET `/test/example.xml?query=param` will call method `_test_example_xml(self, request)`

This can be used via `requests_staticmock.ClassAdapter` or the context manager

.. automodule:: requests_staticmock.context
    :members: mock_session_with_class

Example
+++++++

.. code-block:: python

    import requests
    import requests_staticmock
    
    
    class MyTestClass(requests_staticmock.BaseMockClass):
        def _api_v1_idea(self, request):
            return "woop woop"
    
    session = requests.Session()
    with requests_staticmock.mock_session_with_class(session, MyTestClass, 'http://test_context.com'):
        # will return a response object with the contents 'woop woop'
        response = new_session.request('get', 'http://test_context.com/api/v1/idea')

Class adapter with unpacked requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The class adapter supports unpacking of the following components, just add these keyword arguments
to your callback methods and the class adapter will match them to the arguments.

* `method` - The HTTP verb, e.g. GET
* `url` - The full URL
* `params` - The dict with the request parameters
* `headers` - The request headers
* `body` - The request body text

.. code-block:: python

    import requests
    import requests_staticmock

    class_session = Session()
    class TestMockClass(BaseMockClass):
        def _api_v1_idea(self, method, params, headers):
            if params['special'] == 'value':
                return 'yes'
        def _api_v1_brillo(self, url, body):
            if json.loads(body)['special'] == 'value':
                return 'yes'

    a = ClassAdapter(TestMockClass)
    
    session = requests.Session()
    with requests_staticmock.mock_session_with_class(session, MyTestClass, 'http://test_context.com'):
        response = new_session.request('get', 'http://test_context.com/api/v1/idea')

See StaticResponseFactory for simple ways of returning good and bad responses.

.. autoclass:: requests_staticmock.responses.StaticResponseFactory
    :members:

Features
--------

* Allow mocking of HTTP responses via a directory of static fixtures
* Support for sub-directories matching URL paths

Credits
---------

This project takes inspiration and ideas from the `requests_mock` package, maintained by the OpenStack foundation. I redesigned this based on the abstractions within the requests project instead of using the
patching pattern used in `requests_mock`. I find the responses more native, easier to work with and also the ability to load static files much easier.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
