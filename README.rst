wlint
=====
wlint is a collection of scripts and tools that can be used to help with
writing.  The project is designed for a Unix-like environment.

Dependencies
------------
wlint is designed for a Unix-like environment.  Any modern Linux distribution
should be fine, but OS X and Cygwin shouldn't have any problems either.

To ensure maximum portability, dependencies are kept to a minimum.  Currently
scripts are written in either :code:`/bin/sh` (assumes a typical collection of
standard command line tools) and Python 3 (assumed to be
:code:`/usr/bin/python3`).

Installing
----------
:code:`sh install.sh` Installs to the default prefix [:code:`/usr/local`]

:code:`sh install.sh --prefix=/path/to/prefix` Installs to a custom prefix

Usage
-----
wlint follows the pattern of tools like :code:`git` and
:code:`apt-get`: there's a single front-end (:code:`wlint`) to launch other
tools.  To get a list of tools, use the :code:`--list` option.

Documentation for the other tools is available with the :code:`-h` or
:code:`--help` options, e.g.:

.. code::

   wling list-filter -h
   usage: list-filter [-h] [--lists LISTS] [--list LIST] [--file FILE]
                      [file [file ...]]

