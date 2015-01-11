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

def rpm_attr(ownergroup):
  pair = ownergroup.split(':', 1)
  owner = pair[0] if pair[0] else '-'
  group = pair[1] if pair[1] else '-'
  return "%attr(-, {0}, {1}) ".format(owner, group)

def list_files(buildroot, path, excludes, ownership):
  if path not in excludes:
    prefix = rpm_attr(ownership[path]) if path in ownership else ''
    print(prefix + '"' + path + '"')
  else:
    realpath = buildroot + path
    if os.path.isdir(realpath):
      for name in os.listdir(realpath):
        nextpath = os.path.join(path, name)
        list_files(buildroot, nextpath, excludes, ownership)

if __name__ == "__main__":
  buildroot = sys.argv[1]
  clump = ClumpInfo("clump.yaml")
  list_files(buildroot, '/', path_exclusions(clump), clump.ownership)

