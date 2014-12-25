from __future__ import print_function, division, unicode_literals
import warnings
import os
import argparse
import tarfile
import osrelease
osrelease.sys_path_append_match(os.path.dirname(__file__))
import backend
import common 

def list_files(args):
  backend.print_files_list(args.buildroot)

def main():
  parser = argparse.ArgumentParser(
    description="Cross Linux Uniform Mutual Packager")
  subparsers = parser.add_subparsers(title="clump commands")

  sub_parser = subparsers.add_parser('list-files',
    help="Generate files list for RPM.")
  sub_parser.add_argument('buildroot',
    help="directory of filesystem to package")
  sub_parser.set_defaults(func=list_files)

  args = parser.parse_args()
  args.func(args)

def make(clumpath):
  clump = common.Clump(clumpath)
  tar = tarfile.open(backend.tarball_filepath(clump), "w:gz")
  tar.add(clumpath, clump.name + '-' + clump.version)
  tar.close()
  backend.build(clump)

