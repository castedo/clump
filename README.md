Cross Linux Uniform Mutual Packager
===================================

Clump is a tool for generating both RPM and Debian packages from a single
distro-agnostic source. Clump reads a YAML file similar to RPM spec files and
Debian control files but enables, in a uniform way, functionality found in
both package managers.

It supports a lowest common denominator of functionality that is mutually
supported on both Debian and RPM based package management systems.

Clump is not intended for packages that take advantage of all the
distro-specific features that Debian and RPM package managers offer.
Instead clump is intended for simple packages that only use common
functionality mutually supported in both package managers.

Examples
--------

The [clump.yaml](clump.yaml) in this repository is an example, clump can
package itself using clump. Other examples can be found in the
[clump-examples](https://github.com/castedo/clump-examples) repository.

Notable Features
----------------

#### Automatic RPM file list generation

Clump will automatically deduce a "files list" for an RPM package by looking at
what gets install and then removing paths owned by any required packages and
the "filesystem" package.

#### Uniform specification for both RPM and Debian packages

Data needed for generating RPM and Debian source packages are specified in a uniform
way inside a `clump.yaml` file. In particular:

* RPM packages can declare a user and group for installed files and directories.
  Debian in contrast requires post-installation script to call chown on installed
  paths. Clump allows a declaration of user and group ownership within `clump.yaml`
  of installed paths and clump will generate appropriate RPM or Debian
  post-instalation scripts as appropriate.

* Changelogs for Debian and RPM in their respective formats, get generated by clump
  from the YAML change log inside `clump.yaml`.

#### Package specification that can be parsed by other applications

Rather than procedural code such as Python and shell scripts, a `clump.yaml`
file can be parsed as YAML by other applications.  For instance, a `setup.py`
script can read a `clump.yaml` file to determine package name and version. This
is in fact how the `setup.py` script for clump itself works.

#### Automatic source download

Sources can get automatically downloaded when accompanied by checksums.


Caveats
-------

Clump is experimental at this stage and in use on:
* CentOS 7
* Amazon Linux 2014.09
* Ubuntu 14.04

Clump generates packages for the distribution it is being run on.  For multiple
packages for muliple distributions you need to run clump on those multiple
distributions.

Binary RPM Packages
-------------------

An RPM package named clump is built by Castedo and found in the following repositories:
* CentOS/RHEL 7: http://dist.brokertron.com/repo/centos/7/brokertron.repo
* Amazon Linux 2014.09: http://dist.brokertron.com/repo/amzn/2014.09/brokertron.repo

Place those .repo files in your /etc/yum.repos.d/ and do `sudo yum install clump`.

Or you can git clone this repository and run `clump/test/clump.sh`.

Related Projects
----------------

* [Effing Package Management](http://github.com/jordansissel/fpm)
* [Open Build Service](http://openbuildservice.org)
* [Alien](http://en.wikipedia.org/wiki/Alien_(software))
* [pkgwrite](http://ffem.org/daveb/pkgwrite/)

