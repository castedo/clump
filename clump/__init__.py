from __future__ import print_function, division, unicode_literals
import warnings
import os
from os.path import join
import shutil
import argparse
import tarfile
import osrelease
osrelease.sys_path_append_match(os.path.dirname(__file__))
import backend
from common import ClumpInfo, tarball_topdir

def clump_dir_to_tarball(dirpath):
  clump = ClumpInfo(join(dirpath, "clump.yaml"))
  tarfilepath = join(backend.tarball_dest(), clump.tarfilename)
  tar = tarfile.open(tarfilepath, "w:gz")
  tar.add(dirpath, clump.untardir)
  tar.close()
  return tarfilepath

def clumpball_info(path):
  with tarfile.open(path, "r:gz") as tar:
    entry = join(tarball_topdir(tar), "clump.yaml")
    info = ClumpInfo(tar.extractfile(entry))
  return info

def main():
  parser = argparse.ArgumentParser(
    description="Cross Linux Uniform Mutual Packager")
  parser.add_argument('clumpath',
                      help="Path to source clump directory")
  srcpath = parser.parse_args().clumpath
  if os.path.isdir(srcpath):
    srcpath = clump_dir_to_tarball(srcpath)
  clump = clumpball_info(srcpath)
  tarpath = join(backend.tarball_dest(), clump.tarfilename)
  if not os.path.exists(tarpath) or not os.path.samefile(srcpath, tarpath):
    shutil.copy(srcpath, tarpath)
  backend.build(clump)

