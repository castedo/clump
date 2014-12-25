from __future__ import print_function, division, unicode_literals
import warnings
import os
import subprocess
from string import Template
from subprocess import check_call

def tarball_filename(clump):
  return "{0}-{1}.tar.gz".format(clump.name, clump.version)

def tarball_filepath(clump):
  return os.path.expanduser('~/rpmbuild/SOURCES/') + tarball_filename(clump)

def rpm_changelog(clump):
  ret = ''
  for entry in clump.changelog:
    ret += "* {0} {1} - {2}\n".format(entry['when'], entry['who'], entry['version'])
    ret += "- {0}\n".format(entry['what'])
  return ret

def rpm_sources(clump):
  ret = 'Source:         ' + tarball_filename(clump)
  n = 1
  for c in clump.components:
    ret += '\nSource{0}:        {1}'.format(n, c.file if c.file else c.url)
    n += 1
  return ret

def rpm_prep(clump):
  lines = ['%setup -q']
  n = 1
  for c in clump.components:
    c.save_source(os.path.expanduser('~/rpmbuild/SOURCES/'))
    lines.append("mkdir {0}".format(c.id))
    lines.append("cp %SOURCE{0} {1}".format(n, c.id))
    n += 1
  return '\n'.join(lines)

def rpm_spec_content(clump):
  vals = dict()
  vals['name'] = clump.name
  vals['version'] = clump.version
  vals['summary'] = clump.summary if clump.summary else clump.name
  vals['description'] = clump.description if clump.description else ''
  vals['sources'] = rpm_sources(clump)

  if clump.arch:
    arch = 'noarch' if clump.arch == 'any' else clump.arch
    vals['buildarch'] = 'BuildArch:      ' + arch
  else:
    vals['buildarch'] = ''

  vals['requires'] = ''
  for r in clump.requires:
    vals['requires'] += 'Requires:       ' + r + '\n'

  vals['prep'] = rpm_prep(clump)
  vals['build'] = '%cmake .' + '\n' + 'make'
  vals['install'] = 'make install DESTDIR=%{buildroot}'
  vals['changelog'] = rpm_changelog(clump)

  vals.setdefault('prep', '# no prep')
  vals.setdefault('build', '# no build')
  vals.setdefault('install', '# no installation')

  template_path = os.path.join(os.path.dirname(__file__), 'template-rpm.spec')
  tmpl = Template(open(template_path).read())
  return(tmpl.substitute(vals))

def build(clump):
  name_version = clump.name + '-' + clump.version
  specpath = os.path.expanduser('~/rpmbuild/SPECS/' + name_version + '.spec')
  print(rpm_spec_content(clump), file=open(specpath, "w"))
  check_call(['rpmbuild', '-ba', specpath])

def print_files_list(buildroot):
  output = subprocess.check_output(['rpm', '--query', '--list', 'filesystem'])
  exclude = output.splitlines()
  for (dirpath, dirnames, filenames) in os.walk(buildroot):
    rpath = os.path.relpath(dirpath, buildroot)
    rpath = '/' + rpath if rpath != '.' else ''
    paths = [rpath + '/' + n for n in dirnames]
    for p in paths:
      if p not in exclude:
        print('%dir "' + p + '"')
    paths = [rpath + '/' + n for n in filenames]
    for p in paths:
      if p not in exclude:
        print('"' + p + '"')
