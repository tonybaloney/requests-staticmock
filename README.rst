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


A static HTTP mock interface for requests

* Free software: Apache 2 License
* Documentation: https://requests-staticmock.readthedocs.org.

Usage
-----

As a context manager for requests Session instances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `requests_staticmock`

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


.. code-block:: python

    import requests
    import requests_staticmock
    
    
    class MyTestClass(requests_staticmock.BaseMockClass):
        def _api_v1_idea(self, request):
            return "woop woop"
    
    session = requests.Session()
    with requests_staticmock.mock_session_with_class(session, MyTestClass, 'http://test_context.com'):
        # will return a response object with the contents 'woop woop'
        response = new_session.request('get', 'http://test_context.com/test.json')

Features
--------

* Allow mocking of HTTP responses via a directory of static fixtures
* Support for sub-directories matching URL paths


Credits
---------

This project takes inspiration and ideas from the `requests_mock` package, maintained by the OpenStack foundation.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
