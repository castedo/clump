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
      mi = self.ts.dbMatch(rpm.RPMTAG_PROVIDENAME, requirement)
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
      if not self.ts.dbMatch(rpm.RPMTAG_PROVIDENAME, r).count():
        raise ValueError("Required package is not installed: " + r)
      self.walk(r)

def list_chowned_paths(chowned):
  for path, ownergroup in chowned.iteritems():
    pair = ownergroup.split(':', 1)
    owner = pair[0] if pair[0] else '-'
    group = pair[1] if pair[1] else '-'
    print('%attr(-, {0}, {1}) "{2}"'.format(owner, group, path))

def list_simple_paths(buildroot, path, external, skips):
  realpath = buildroot + path
  if os.path.isdir(realpath) and path in external:
    for name in os.listdir(realpath):
      nextpath = os.path.join(path, name)
      if not nextpath in skips:
        list_simple_paths(buildroot, nextpath, external, skips)
  else:
    print('"' + path + '"')

if __name__ == "__main__":
  buildroot = sys.argv[1]
  clump = ClumpInfo("clump.yaml")
  walker = DependencyWalker()
  walker.walk_all(clump.requires + ['filesystem'])
  list_simple_paths(buildroot, '/', walker.files, clump.ownership.keys())
  list_chowned_paths(clump.ownership)

