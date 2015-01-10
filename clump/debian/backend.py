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

def tarball_dest():
  return "."

def build_dir():
  return "."

def debian_rules(clump):
  vals = dict()
  if clump.install:
    vals['build'] = '# no build'
    vals['install'] = ( "export DESTDIR=debian/" + clump.name +
                        '\n\t' + "clumpiled/install.sh" )
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
    ret += "  * {0}\n".format(entry['what'])
    ret += " -- {0}  {1}\n".format(entry['who'], when)
  return ret

def debian_postinst(clump):
  lines = []
  for path in clump.ownership:
    ownergroup = clump.ownership[path]
    lines.append("chown --recursive {0} '{1}'".format(ownergroup, path))
  vals = { 'chownlines': "\n".join(lines) }
  template_path = os.path.join(MODULE_PATH, 'template-postinst')
  tmpl = string.Template(open(template_path).read())
  return(tmpl.substitute(vals))

def save_components(clump):
  for c in clump.components:
    tarball = path.join('..', c.debian_tarball_filename(clump))
    if c.file:
      filepath = path.join('..', c.file)
      c.save_source(filepath)
      with tarfile.open(tarball, "w:gz") as tar:
        tar.add(filepath, path.join(c.id, c.file))
    else:
      c.save_source(tarball)
    with tarfile.open(tarball, "r") as tar:
      tar.extractall()

def build(clump):
  if path.exists(clump.untardir):
    shutil.rmtree(clump.untardir)
  with tarfile.open(clump.tarfilename, "r") as tar:
    tar.extractall()
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
  save_components(clump)
  check_call(['debuild', '-uc', '-us'])

def print_files_list(buildroot):
  sys.exit("print_files_list not implemented on this distro")

