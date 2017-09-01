=======
History
=======


1.4.0 (2017-09-01)
------------------

* Class adapter correctly maps - character to _ as - is invalid method name in Python

1.3.0 (2017-09-01)
------------------

* Add a property in MockClass for the adapter instance, helps when you want to respond
  with static fixture data

1.2.0 (2017-05-10)
------------------

* Add support for case-insensitive file matching

1.1.0 (2017-05-10)
------------------

* Add support for query params being part of the file path

0.8.0 (2017-02-02)
------------------

* Add support for streaming requests and iter_content/iter_lines

0.7.0 (2017-01-29)
------------------

* Add support version unpacking, class adapters now support a range of keyword arguments,
  provided in no particular order.

0.6.0 (2017-01-29)
------------------

* Add support for the class adapter methods to return either a string or
  a response object
* Moved to Py.Test

0.3.0 (2017-01-29)
------------------

* Added a class adapter

0.2.0 (2017-01-28)
------------------

* Added a context manager for the static mocks

0.1.0 (2017-01-01)
------------------

* First release on PyPI.
