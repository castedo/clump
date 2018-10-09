from __future__ import print_function, division, unicode_literals
import warnings
import os
from os.path import join
import distutils.dir_util
import time
from string import Template
from subprocess import check_call
from clump import common

def tarball_dest():
  dest = os.path.expanduser('~/rpmbuild/SOURCES/')
  distutils.dir_util.mkpath(dest)
  return dest

def build_dir():
  dest = os.path.expanduser('~/rpmbuild/BUILD/')
  distutils.dir_util.mkpath(dest)
  return dest

def specs_dest():
  dest = os.path.expanduser('~/rpmbuild/SPECS/')
  distutils.dir_util.mkpath(dest)
  return dest

def rpm_changelog(clump):
  ret = ''
  for entry in clump.changelog:
    s = "* {0} {1} - {2}\n"
    when = time.strftime("%a %b %d %Y", entry.when)
    ret += s.format(when, entry.who, entry.version)
    ret += "- {0}\n".format(entry.what)
  return ret

def rpm_sources(clump):
  ret = 'Source:         ' + clump.tarfilename
  n = 1
  for c in clump.components:
    ret += '\nSource{0}:        {1}'.format(n, c.file if c.file else c.url)
    n += 1
  return ret

def rpm_prep(clump):
  lines = ['%setup -q']
  n = 1
  for c in clump.components:
    if c.file:
      outpath = tarball_dest() + c.file
      c.save_source(outpath)
      lines.append("mkdir {0}".format(c.id))
      lines.append("cp %SOURCE{0} {1}".format(n, c.id))
    else:
      fn = c.url.split('/')[-1]
      if not fn:
        fn = c.debian_tarball_filename(clump)
      outpath = tarball_dest() + fn
      c.save_source(outpath)
      untardir = common.tarball_topdir(outpath)
      lines.append("%setup -q -T -D -a {0}".format(n))
      lines.append("mv {0} {1}".format(untardir, c.id))
    n += 1
  return '\n'.join(lines)

def rpm_spec_content(clump):
  vals = dict()
  vals['name'] = clump.name
  vals['version'] = clump.version
  vals['summary'] = clump.summary if clump.summary else clump.name
  vals['description'] = clump.description if clump.description else ''
  vals['pre'] = clump.pre or ""
  vals['post'] = clump.post or ""
  vals['sources'] = rpm_sources(clump)

  if clump.arch and clump.arch != 'any':
    arch = 'noarch' if clump.arch == 'all' else clump.arch
    vals['buildarch'] = 'BuildArch:      ' + arch
  else:
    vals['buildarch'] = ''

  vals['requires'] = ''
  for r in clump.requires:
    vals['requires'] += 'Requires:       ' + r + '\n'

  vals['buildrequires'] = ''
  for r in clump.buildrequires:
    vals['buildrequires'] += 'BuildRequires:       ' + r + '\n'

  vals['prep'] = rpm_prep(clump)
  vals['changelog'] = rpm_changelog(clump)

  if clump.install:
    vals['build'] = '# no build'
    vals['install'] = ( "export DESTDIR=%{buildroot}" +
                        '\n' + "clumpiled/install.sh" )
  else:
    vals['build'] = '%cmake .' + '\n' + 'make'
    vals['install'] = 'make install DESTDIR=%{buildroot}'

  template_path = join(os.path.dirname(__file__), 'template-rpm.spec')
  tmpl = Template(open(template_path).read())
  return(tmpl.substitute(vals))

def build(clump):
  name_version = clump.name + '-' + clump.version
  specpath = specs_dest() + name_version + '.spec'
  print(rpm_spec_content(clump), file=open(specpath, "w"))
  check_call(['rpmbuild', '-ba', specpath])

