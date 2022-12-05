#!/usr/bin/env python

from setuptools import setup, find_namespace_packages

gql = ['graphql>=0.0.4','graphql_core>=3.2.3']
all_pkgs = gql

setup(name='Toadstool',
      version='0.1.0',
      description='Python Load Tools Suite',
      author='Andrés Alejos',
      author_email='acalejos@proton.me',
      url='https://github.com/acalejos/toadstool/',
      packages=['toadstool'],
      extras_require = {
            "gql": gql,
            'all': all_pkgs
      },
      package_dir={'toadstool':'src'}
     )

