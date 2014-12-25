from __future__ import print_function, division, unicode_literals
import warnings
import os
import sys
from configobj import ConfigObj

os_release = ConfigObj('/etc/os-release')

ID = os_release['ID']
VERSION_ID = os_release['VERSION_ID']
IDS = [ID] + os_release['ID_LIKE'].split(' ')

def sys_path_append_match(dir_path):
  for distro in IDS:
    backend_path = os.path.join(dir_path, distro)
    if os.path.exists(backend_path):
      sys.path.append(backend_path)
      return True
  return False

