#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests', 'six'
]

test_requirements = [
   'pytest'
]

setup(
    name='requests-staticmock',
    version='0.8.0',
    description="A static HTTP mock interface for requests",
    long_description=readme + '\n\n' + history,
    author="Anthony Shaw",
    author_email='anthonyshaw@apache.org',
    url='https://github.com/tonybaloney/requests-staticmock',
    packages=[
        'requests_staticmock',
    ],
    package_dir={'requests_staticmock':
                 'requests_staticmock'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache License (2.0)",
    zip_safe=False,
    keywords='requests_staticmock',
     classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'],
    tests_require=test_requirements,
    setup_requires=['pytest-runner']
)
