#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from django_etl import __version__ as version

long_description = 'Please see the documentation at the `project page <https://github.com/PGower/django_etl>`_ .'

packages = [
    'django_etl',
    'django_etl.management',
    'django_etl.management.commands',
]

package_data = {
    '': ['LICENSE', 'README.md'],
}

# with open('README.md') as f:
#     readme = f.read()

setup(
    name='django_etl',
    version=version,
    description='A Django application that provides a management command to make using the petl library easier.',
    long_description=long_description,
    author='Paul Gower',
    author_email='p.gower@gmail.com',
    url='https://github.com/PGower/django_etl',
    download_url='https://github.com/PGower/django_etl/releases',
    package_dir={'django_etl': 'django_etl'},
    packages=packages,
    package_data=package_data,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['django', 'petl', 'etl', 'synchronize', 'sync', 'extract', 'transform', 'load'],
    install_requires=['petl >= 1.0.11'],
)
