from __future__ import print_function, division, unicode_literals
import warnings
import os
import tarfile
import osrelease
osrelease.sys_path_append_match(os.path.dirname(__file__))
import backend
import common 

def make(clumpath):
  clump = common.Clump(clumpath)
  tar = tarfile.open(backend.tarball_filepath(clump), "w:gz")
  tar.add(clumpath, clump.name + '-' + clump.version)
  tar.close()
  backend.build(clump)

def print_files_list(buildroot):
  backend.print_files_list(buildroot)

