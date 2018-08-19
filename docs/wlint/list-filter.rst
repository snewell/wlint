list-filter
===========

--------------------------------
detect words that weaken writing
--------------------------------

.. BEGIN_MAN_SECTION

:Author: Stephen Newell
:Copyright: BSD Two-Clause
:Version: 0.1.0
:Manual section: 1
:Manual group: wlint manual

.. END_MAN_SECTION


Synopsis
--------
::

    wlint list-filter [-h] [--input-type INPUT_TYPE] [--list-input-types]
                      [--lists LISTS] [--list LIST] [--sort SORT]
                      [--list-sorts]
                      [file [file ...]]


Description
-----------
Each instance of a word in the filter lists will be displayed, along with the
line and column.  Example output looks like this:

::

    sample-input.txt a bit (23:587)
    sample-input.txt a bit (53:496)
    sample-input.txt a bit (55:611)
    sample-input.txt actually (49:22)
    sample-input.txt began (13:215)
    sample-input.txt begin (3:1)
    sample-input.txt certainly (51:317)
    sample-input.txt completely (39:471)
    sample-input.txt could (15:72)
    sample-input.txt could (19:628)

If no files are specified, input is read via standard input.


Options
-------
  -h, --help            show this help message and exit
  --input-type INPUT_TYPE
                        Type of input file. (default: text)
  --list-input-types    List supported input types.
  --lists LISTS         Change the set of word lists. This should be a comma-
                        separated list of built-in lists. (default:
                        filter,thought,weasel)
  --list LIST           Use a custom word list. The list should be a plain
                        text file with one word per line. (default: None)
  --sort SORT           Method to sort output. Options are: alpha, sequential
                        (default: alpha)
  --list-sorts          List supported sort methods.


Word Lists
----------
Word lists consist of one entry per line.  Entries can contain symbols and
white space and symbols, but are matched *exactly* against the contents of any
files be scanned.  The following are all valid entries in a word list file:

- a bit
- looked
- that's

Matches are case-insensitive, so "a bit," "a BIT," and "A bIt" would all be
picked up by the first entry in the sample list.  Likewise, "that's" will
match a string of characters with a single-quote, not an apostrophe.


Sort Methods
------------
alpha
    Sort output based on the actual words.  This is useful if trying to deal
    with all instances of a given word (e.g., you're trying to reduce a word or
    phrase you use as a crutch).
sequential
    Sort output based on the order words appear.  This is useful when you're
    working on general editing, since you can start at the top of the output
    and work your way down both the output and your document at the same time.
