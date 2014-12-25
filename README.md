clump - Cross Linux Unrefined Mutual Packager
=============================================

Clump is a tool for generating both RPM and Debian packages from a single
distro-agnostic source. Clump reads a YAML file similar to RPM spec files and
Debian control files but enables in a uniform way functionality found in
both package managers.

It supports a lowest common denominator of functionality that is mutually
supported on both Debian and RPM based package management systems.

Clump is not intended for **"refined"** packages that are meant to take advantages
of all the special powerful features that Debian and RPM package managers offer.
Instead clump is intended for **"unrefined"** packages that only use common
functionality supported in both package managers.

Caveats
-------

Clump is experimental at this stage and in use on CentOS 7 and Ubuntu 14.04.


Other Similar Projects
----------------------

* [Effing Package Management](http://github.com/jordansissel/fpm)
* [Open Build Service](http://openbuildservice.org)
* [Alien](http://en.wikipedia.org/wiki/Alien_(software))
* [pkgwrite](http://ffem.org/daveb/pkgwrite/)

