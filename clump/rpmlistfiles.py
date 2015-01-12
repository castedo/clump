#!/usr/bin/python -t
from __future__ import print_function, division, unicode_literals
import warnings
import os
import sys
import rpm
from clump.common import ClumpInfo

class DependencyWalker(object):
  def __init__(self):
    self.ts = rpm.TransactionSet()
    self.walked = set()
    self.files = set()

  def walk(self, requirement):
    if requirement not in self.walked:
      mi = walker.ts.dbMatch(rpm.RPMTAG_PROVIDENAME, requirement)
      for i in range(mi.count()):
        h = mi.next()
        self.files.update(h[rpm.RPMTAG_FILENAMES])
        name = h[rpm.RPMTAG_NAME]
        if name not in self.walked:
          self.walked.add(name)
          rnames = h[rpm.RPMTAG_REQUIRENAME]
          rflags = h[rpm.RPMTAG_REQUIREFLAGS]
          for i in range(len(rnames)):
            if not (rflags[i] & rpm.RPMSENSE_RPMLIB):
              self.walk(rnames[i])

  def walk_all(self, requires):
    for r in requires:
      self.walk(r)

def rpm_attr(ownergroup):
  pair = ownergroup.split(':', 1)
  owner = pair[0] if pair[0] else '-'
  group = pair[1] if pair[1] else '-'
  return "%attr(-, {0}, {1}) ".format(owner, group)

def list_files(buildroot, path, excludes, ownership):
  line = '"' + path + '"'
  if path in ownership:
    line = rpm_attr(ownership[path]) + line
  realpath = buildroot + path
  if not os.path.isdir(realpath):
    print(line)
  else:
    if path not in excludes:
      print(line)
    else:
      for name in os.listdir(realpath):
        nextpath = os.path.join(path, name)
        list_files(buildroot, nextpath, excludes, ownership)

if __name__ == "__main__":
  buildroot = sys.argv[1]
  clump = ClumpInfo("clump.yaml")
  walker = DependencyWalker()
  walker.walk_all(clump.requires + ['filesystem'])
  list_files(buildroot, '/', walker.files, clump.ownership)

