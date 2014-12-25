#!/usr/bin/env python

from distutils.core import setup

setup(name='clump',
      version='0.1',
      description='Cross Linux Unrefined Mutual Packager',
      author='Castedo Ellerman',
      author_email='castedo@castedo.com',
      license='MIT',
      packages=['clump'],
      url='https://github.com/castedo/clump',
      package_data={'clump': ['rhel/*', 'debian/*']},
      scripts=['scripts/clump']
)

