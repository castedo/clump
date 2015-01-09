#!/usr/bin/python -t
from __future__ import print_function, division, unicode_literals
import warnings
import os
import sys
import subprocess
from clump.common import ClumpInfo

# subprocess.check_output is not in Python 2.6
# http://stackoverflow.com/a/13160748/2420027
if "check_output" not in dir(subprocess):
  def check_output(cmd_line):
    proc = subprocess.Popen(rpm_cmd_line, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    retcode = proc.poll()
    if retcode:
      raise subprocess.CalledProcessError(retcode, cmd_line)
    return output
else:
  from subprocess import check_output

def path_exclusions(clump):
  excludes = ['filesystem']
  excludes += list(set(clump.requires) & set(clump.buildrequires))
  rpm_cmd_line = ['rpm', '--query', '--list'] + excludes
  output = check_output(rpm_cmd_line)
  return output.splitlines()

class OwnershipCursor(object):
  def __init__(self, ownership):
    self.ownership = ownership
    self.owner = None
    self.group = None

  def rpm_attr(self):
    if self.owner or self.group:
      owner = self.owner if self.owner else '-'
      group = self.group if self.group else '-'
      return "%attr(-, {0}, {1}) ".format(owner, group)
    return ''

  def select(self, path):
    ret = self
    if path in self.ownership:
      pair = self.ownership[path].split(':', 1)
      ret = OwnershipCursor(self.ownership)
      if pair[0]:
        ret.owner = pair[0]
      if pair[1]:
        ret.group = pair[1]
    return ret

def list_files(buildroot, path, excludes, cursor):
  realpath = buildroot + path
  if path not in excludes:
    cursor = cursor.select(path)
    prefix = cursor.rpm_attr()
    if os.path.isdir(realpath):
      prefix += '%dir '
    print(prefix + '"' + path + '"')
  if os.path.isdir(realpath):
    for name in os.listdir(realpath):
      nextpath = os.path.join(path, name)
      list_files(buildroot, nextpath, excludes, cursor)

if __name__ == "__main__":
  buildroot = sys.argv[1]
  clump = ClumpInfo("clump.yaml")
  cursor = OwnershipCursor(clump.ownership)
  list_files(buildroot, '/', path_exclusions(clump), cursor)

