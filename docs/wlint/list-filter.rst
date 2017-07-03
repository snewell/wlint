list-filter
===========
list-filter is a tool to detect words that weaken writing.

Usage
-----
:code:`list-filter [options] file [file ...]`

Each instance of a word in the filter lists will be displayed, along with the
line and column.  Example output looks like this:

::

    A-00prologue.tex a bit (23:587)
    A-00prologue.tex a bit (53:496)
    A-00prologue.tex a bit (55:611)
    A-00prologue.tex actually (49:22)
    A-00prologue.tex began (13:215)
    A-00prologue.tex begin (3:1)
    A-00prologue.tex certainly (51:317)
    A-00prologue.tex completely (39:471)
    A-00prologue.tex could (15:72)
    A-00prologue.tex could (19:628)

Options
-------
-h, --help            show this help message and exit
--file FILE           Process a file. This is only necessary if an input
                      file matches an argument (e.g., --help).
--stdin               Parse stdin. If both files and this option are used,
                      files are processed before stdin.
--lists LISTS         Change the set of word lists. This should be a comma-
                      separated list of built-in lists.
                      [Default=filter,thought,weasel]
--list LIST           Use a custom word list. The list should be a plain
                      text file with one word per line.
--sort-method SORT_METHOD
                      Method to sort discovered words. Options are alpha
                      (filter words are alphabetized and grouped) and
                      sequential (the order words appear in input). The
                      default is alpha.

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
