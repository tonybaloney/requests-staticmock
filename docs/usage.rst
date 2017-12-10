
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
