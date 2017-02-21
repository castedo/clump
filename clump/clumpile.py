#!/usr/bin/python -t
from __future__ import print_function, division, unicode_literals
import os
from os import path
import shutil
import distutils.dir_util
from clump.common import ClumpInfo

MODULE_PATH = path.abspath(path.dirname(__file__))

def write_bash_script(content, filename):
  path = "clumpiled/" + filename
  with open(path, 'w') as fout:
    print("#!/bin/bash", file=fout)
    print("set -o errexit", file=fout)
    print(content, file=fout)
  os.chmod(path, 0755)

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
    write_bash_script(clump.install, "install.sh")

