from __future__ import print_function, division, unicode_literals
import warnings
import os
import argparse
import tarfile
import osrelease
osrelease.sys_path_append_match(os.path.dirname(__file__))
import backend
import common 

def get_buildroot():
  parser = argparse.ArgumentParser(description='Generate files list for RPM.')
  parser.add_argument('buildroot', help="directory of filesystem to package")
  args = parser.parse_args()
  return args.buildroot

def main():
  print_files_list(get_buildroot())

def make(clumpath):
  clump = common.Clump(clumpath)
  tar = tarfile.open(backend.tarball_filepath(clump), "w:gz")
  tar.add(clumpath, clump.name + '-' + clump.version)
  tar.close()
  backend.build(clump)

def print_files_list(buildroot):
  backend.print_files_list(buildroot)

