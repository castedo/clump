from __future__ import print_function, division, unicode_literals
import warnings
import os
import osrelease
import yaml
import urllib
import hashlib
import tarfile

def tarball_topdir(tar):
  if not isinstance(tar, tarfile.TarFile):
    with tarfile.open(tar, "r") as obj:
      return tarball_topdir(obj)
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
      if type(requirement) is dict:
        for id in osrelease.IDS:
          if id in requirement:
            requirement = requirement[id]
            break
      ret.append(requirement)
  return ret

def file_digest(filepath, hashobj):
  with open(filepath, 'rb') as f:
    while True:
      chunk = f.read(4096)
      if chunk:
        hashobj.update(chunk)
      else:
        return hashobj.hexdigest()

class Component(object):
  def __init__(self, id, values):
    self.id = id
    self.url = values.get('url')
    self.sha1 = values.get('sha1')
    self.file = values.get('file')

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

class ClumpInfo(object):

  def __init__(self, yamlfile):
    if isinstance(yamlfile, unicode):
      yamlfile = open(yamlfile)
    content = yaml.load(yamlfile, yaml.BaseLoader)
    yamlfile.close()
    content = dict((k.lower(), content[k]) for k in content)

    self.name = content.get('name')
    if not self.name:
      raise ValueError("'name:' value is required in clump file")
    self.release = content.get('release', 0)
    self.arch = content.get('arch')
    self.summary = content.get('summary')
    self.description = content.get('description')
    self.requires = resolve_requires(content.get('requires'))
    self._init_changelog(content)
    self._init_version(content)
    self._init_sources(content)
    self.tarfilename = "{0}_{1}.orig.tar.gz".format(self.name, self.version)
    self.untardir = "{0}-{1}".format(self.name, self.version)

  def _init_changelog(self, content):
    self.changelog = content.get('changelog')
    if not self.changelog or not len(self.changelog):
      raise ValueError("'changelog:' non-empty list is required in clump file")

  def _init_version(self, content):
    self.version = self.changelog[0].get('version')
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

