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
from clump import common

MODULE_PATH = path.abspath(path.dirname(__file__))

def tarball_dest():
  return "."

def build_dir():
  return "."

def debian_rules(clump):
  vals = dict()
  if clump.install:
    vals['build'] = '# no build'
    destdir = "debian/" + clump.name
    vals['install'] = "DESTDIR={0} clumpiled/install.sh".format(destdir)
  else:
    vals['build'] = 'cmake .' + '\n\t' + 'make'
    vals['install'] = "make install DESTDIR=debian/" + clump.name

  template_path = path.join(MODULE_PATH, 'template-rules')
  tmpl = string.Template(open(template_path).read())
  return(tmpl.substitute(vals))

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
    body_text = "\n    ".join(entry['what'].splitlines())
    ret += "  * {0}\n".format(body_text)
    ret += " -- {0}  {1}\n".format(entry['who'], when)
  return ret

def debian_postinst(clump):
  lines = []
  for path in clump.ownership:
    ownergroup = clump.ownership[path]
    lines.append("chown --recursive {0} '{1}'".format(ownergroup, path))
  vals = { 'chownlines': "\n".join(lines) }
  template_path = path.join(MODULE_PATH, 'template-postinst')
  tmpl = string.Template(open(template_path).read())
  return(tmpl.substitute(vals))

def save_components(clump, destpath):
  for c in clump.components:
    tarball = c.debian_tarball_filename(clump)
    component_dir = path.join(destpath, c.id)
    if c.file:
      c.save_source(c.file)
      with tarfile.open(tarball, "w:gz") as tar:
        tar.add(c.file, path.join(c.id, c.file))
      os.mkdir(component_dir)
      shutil.copy(c.file, component_dir)
    else:
      c.save_source(tarball)
      with tarfile.open(tarball, "r") as tar:
        tar.extractall(path=destpath)
        topdir = common.tarball_topdir(tar)
      os.rename(path.join(destpath, topdir), component_dir)

def build(clump):
  if path.exists(clump.untardir):
    shutil.rmtree(clump.untardir)
  with tarfile.open(clump.tarfilename, "r") as tar:
    tar.extractall()
  save_components(clump, clump.untardir)
  os.chdir(clump.untardir)
  os.mkdir('debian')
  print("9", file=open('debian/compat', 'w'))
  print("Format: about:blank", file=open('debian/copyright', 'w'))
  print(debian_rules(clump), file=open('debian/rules', 'w'))
  os.chmod('debian/rules', 0755)
  print(debian_control(clump), file=open('debian/control', 'w'))
  print(debian_changelog(clump), file=open('debian/changelog', 'w'))
  if clump.ownership:
    print(debian_postinst(clump), file=open('debian/postinst', 'w'))
  os.mkdir('debian/source')
  print("3.0 (quilt)", file=open('debian/source/format', 'w'))
  check_call(['debuild', '-uc', '-us'])

def print_files_list(buildroot):
  sys.exit("print_files_list not implemented on this distro")

