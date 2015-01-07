#!/usr/bin/python -t
from __future__ import print_function, division, unicode_literals
import os
from os import path
import shutil
import distutils.dir_util
from clump.common import ClumpInfo

MODULE_PATH = path.abspath(path.dirname(__file__))

if __name__ == "__main__":
  clump = ClumpInfo("clump.yaml")
  distutils.dir_util.mkpath("clumpiled")
  if clump.cmake:
    with open("clumpiled/install.cmake", 'w') as fout:
      print(clump.cmake, file=fout)
    if not os.path.exists("CMakeLists.txt"):
      srcpath = path.join(MODULE_PATH, "default-CMakeLists.txt")
      shutil.copy(srcpath, "CMakeLists.txt")
  elif clump.install:
    with open("clumpiled/install.sh", 'w') as fout:
      print("#!/bin/bash", file=fout)
      print(clump.install, file=fout)
    os.chmod("clumpiled/install.sh", 0755)

