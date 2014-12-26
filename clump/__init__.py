from __future__ import print_function, division, unicode_literals
import warnings
import os
import argparse
import tarfile
import osrelease
osrelease.sys_path_append_match(os.path.dirname(__file__))
import backend
import common 

def main():
  parser = argparse.ArgumentParser(
    description="Cross Linux Uniform Mutual Packager")
  parser.add_argument('clumpath',
                      help="Path to source clump directory")
  args = parser.parse_args()
  clump = common.Clump(args.clumpath)
  tar = tarfile.open(backend.tarball_filepath(clump), "w:gz")
  tar.add(args.clumpath, clump.name + '-' + clump.version)
  tar.close()
  backend.build(clump)

