from __future__ import print_function, division, unicode_literals
import warnings
import os
import osrelease
import yaml
import time
import urllib
import hashlib
import tarfile

def tarball_topdir(tar):
  if not isinstance(tar, tarfile.TarFile):
    obj = tarfile.open(tar, "r")
    ret = tarball_topdir(obj)
    obj.close()
    return ret
  ret = None
  for entry in tar:
    if len(os.path.dirname(entry.name)) == 0:
      if entry.isdir() and not ret:
        ret = entry.name
      else:
        raise Exception("tar file not a proper tarball")
  return ret

def resolve_requires(requires):
  ret = list()
  if requires:
    for requirement in requires:
      if not type(requirement) is dict:
        ret.append(requirement)
      else:
        for id in osrelease.IDS:
          if id in requirement:
            found = requirement[id]
            break
        if not isinstance(found, list):
          found = [found]
        ret.extend(found)
  return ret

def file_digest(filepath, hashobj):
  f = open(filepath, 'rb')
  while True:
    chunk = f.read(4096)
    if chunk:
      hashobj.update(chunk)
    else:
      f.close()
      return hashobj.hexdigest()
  f.close()

class Component(object):
  def __init__(self, id, values):
    self.id = id
    self.url = values.get('url')
    self.sha1 = values.get('sha1')
    self.file = values.get('file')

  def debian_tarball_filename(self, clump):
    tarsuffix = ".gz"
    pair = self.url.rsplit(".tar", 1)
    if len(pair) == 2:
      tarsuffix = pair[1]
    fn = "{0}_{1}.orig-{2}.tar{3}"
    return fn.format(clump.name, clump.version, self.id, tarsuffix)

  def save_source(self, outpath):
    if not os.path.exists(outpath):
      if not self.sha1:
        raise NotImplementedError("only SHA1 supported right now")
      print(outpath + " <- " + self.url)
      urllib.urlretrieve(self.url, outpath)

    if self.sha1:
      if self.sha1 != file_digest(outpath, hashlib.sha1()):
        msg = ( "hash digest of downloaded file does not match"
              + " hash digest in clump file")
        raise ValueError(msg)

class Change(object):
  def __init__(self, values):
    self.version = values.get('version')
    self.what = values.get('what')
    self.who = values.get('who')
    try:
      # parse RPM style date
      self.when = time.strptime(values.get('when'), "%a %b %d %Y")
    except ValueError:
      msg = "Not in Sat Jan 01 2000 date format: {0}"
      raise ValueError(msg.format(values.get('when')))

def infer_missing_changelog_whos(changelog):
  if not len(changelog):
    raise ValueError("changelog must not be empty")
  inferred = changelog[0].who
  if not inferred:
    raise ValueError("first changelog entry must state who")
  for i in range(1, len(changelog)):
    if changelog[i].who:
      inferred = changelog[i].who
    else:
      next = None
      if i+1 < len(changelog):
        next = changelog[i+1].who
      if next and next != inferred:
        msg = "omitted who is ambiguous (version {0})"
        raise ValueError(msg.format(changelog[i].version))
      changelog[i].who = inferred

class ClumpInfo(object):

  def __init__(self, yamlfile):
    if isinstance(yamlfile, unicode) or isinstance(yamlfile, str):
      yamlfile = open(yamlfile)
    content = yaml.load(yamlfile, yaml.BaseLoader)
    yamlfile.close()
    content = dict((k.lower(), content[k]) for k in content)

    self.name = content.get('name')
    if not self.name:
      raise ValueError("'name:' value is required in clump file")
    self.arch = content.get('arch')
    self.summary = content.get('summary')
    self.description = content.get('description')
    self.cmake = content.get('cmake')
    self.install = content.get('install')
    self.pre = content.get('pre')
    self.post = content.get('post')
    self.requires = resolve_requires(content.get('requires'))
    self.buildrequires = resolve_requires(content.get('buildrequires'))
    self._init_changelog(content)
    self._init_version(content)
    self._init_sources(content)
    self._init_ownership(content)
    self.tarfilename = "{0}_{1}.orig.tar.gz".format(self.name, self.version)
    self.untardir = "{0}-{1}".format(self.name, self.version)

  def _init_changelog(self, content):
    if not 'changelog' in content:
      raise ValueError("changelog missing in clump file")
    self.changelog = [Change(c) for c in content.get('changelog')]
    infer_missing_changelog_whos(self.changelog)

  def _init_version(self, content):
    self.version = self.changelog[0].version
    if not self.version:
      raise ValueError("first changelog entry must have the version")
    if 'version' in content:
      if content['version'] != self.version:
        raise ValueError("version is set to first changelog entry version")

  def _init_sources(self, content):
    self.components = list()
    if 'components' in content:
      for k, v in content['components'].iteritems():
        self.components.append(Component(k, v))

  def _init_ownership(self, content):
    self.ownership = dict()
    if 'ownership' in content:
      for k, v in content['ownership'].iteritems():
        if k[-1] == '/':
          raise ValueError("do not end directory paths with '/'")
        for x in self.ownership:
          if x.startswith(k) or k.startswith(x):
            raise ValueError("nested ownership paths not supported")
        self.ownership[k] = v


