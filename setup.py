#!/usr/bin/env python

import sys
from clump import osrelease

if 'debian' in osrelease.IDS and sys.argv[1] == 'install':
  sys.argv.append("--install-layout=deb")

from distutils.core import setup
from clump.common import ClumpInfo

clump = ClumpInfo("clump.yaml")

setup(name=clump.name,
      version=clump.version,
      description=clump.summary,
      author='Castedo Ellerman',
      author_email='castedo@castedo.com',
      license='MIT',
      packages=['clump'],
      url='https://github.com/castedo/clump',
      package_data={'clump': ['rhel/*', 'debian/*']},
      requires=['yaml', 'configobj'],
      scripts=['scripts/clump']
)

