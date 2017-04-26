# writing-tools
writing-tools is a collection of scripts and tools that can be used to help
with writing.  The project is designed for a Unix-like environment.

## Dependencies
writing-tools is designed for a Unix-like environment.  Any modern Linux
distribution should be fine, but OS X and Cygwin shouldn't have any problems
either.

To ensure maximum portability, dependencies are kept to a minimum.  Currently
scripts are written in either `/bin/sh` (assumes a typical collection of standard
command line tools) and Python 3 (assumed to be `/usr/bin/python3`).

## Installing
`sh install.sh` Installs to the default prefix [`/usr/local`]
`sh install.sh --prefix=/path/to/prefix` Installs to a custom prefix
