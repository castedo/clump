from __future__ import print_function, division, unicode_literals
import warnings
import os
from os import path
import sys
import shutil
import tarfile
import string
import time
from subprocess import check_call

MODULE_PATH = path.abspath(path.dirname(__file__))

def tarball_filename(clump):
  return "{0}_{1}.orig.tar.gz".format(clump.name, clump.version)

def tarball_filepath(clump):
  return tarball_filename(clump)

def debian_rules():
  return(open(path.join(MODULE_PATH, 'rules')).read())

def debian_control(clump):
  vals = dict()
  vals['name'] = clump.name
  vals['summary'] = clump.summary if clump.summary else clump.name

  if clump.description:
    lines = string.split(clump.description, '\n')
    vals['description'] = ' ' + string.join(lines, '\n ')
  vals.setdefault('description', '')

  if clump.arch:
    vals['arch'] = clump.arch if clump.arch != 'noarch' else 'all'
  vals.setdefault('arch', 'any')

  vals['depends'] = ''
  for d in clump.requires:
    vals['depends'] += d.lower() + ', '

  template_path = path.join(MODULE_PATH, 'template-control')
  tmpl = string.Template(open(template_path).read())
  return(tmpl.substitute(vals))

def debian_changelog(clump):
  ret = ''
  for entry in clump.changelog:
    try:
      # parse RPM style date
      when = time.strptime(entry['when'], "%a %b %d %Y")
      # print as debian style date-time
      when = time.strftime("%a, %d %b %Y 00:00:00 +0000", when)
    except ValueError:
      when = entry['when']
    version = entry['version']
    ret += "{0} ({1}-1) UNRELEASED; urgency=low\n".format(clump.name, version)
    ret += "  * {0}\n".format(entry['what'])
    ret += " -- {0}  {1}\n".format(entry['who'], when)
  return(ret)

def build(clump):
  name_version = clump.name + '-' + clump.version
  if path.exists(name_version):
    shutil.rmtree(name_version)
  tar = tarfile.open(tarball_filepath(clump), "r:gz")
  tar.extractall()
  tar.close()
  os.chdir(name_version)
  os.mkdir('debian')
  print("9", file=open('debian/compat', 'w'))
  print("Format: about:blank", file=open('debian/copyright', 'w'))
  print(debian_rules(), file=open('debian/rules', 'w'))
  os.chmod('debian/rules', 0755)
  print(debian_control(clump), file=open('debian/control', 'w'))
  print(debian_changelog(clump), file=open('debian/changelog', 'w'))
  os.mkdir('debian/source')
  print("3.0 (quilt)", file=open('debian/source/format', 'w'))
  check_call(['debuild', '-uc', '-us'])

def print_files_list(buildroot):
  sys.exit("print_files_list not implemented on this distro")

