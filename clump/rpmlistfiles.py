#!/usr/bin/python -t
from __future__ import print_function, division, unicode_literals
import warnings
import os
import sys
import subprocess

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

def list_files(buildroot, path, exclude):
  if path not in exclude:
    print('"' + path + '"')
  else:
    realpath = buildroot + path
    if os.path.isdir(realpath):
      for name in os.listdir(realpath):
        list_files(buildroot, os.path.join(path, name), exclude)

if __name__ == "__main__":
  buildroot = sys.argv[1]
  rpm_cmd_line = ['rpm', '--query', '--list'] + sys.argv[2:]
  output = check_output(rpm_cmd_line)
  exclude = output.splitlines()
  list_files(buildroot, '/', exclude)
