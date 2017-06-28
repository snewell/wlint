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
-h, --help      Display a help message
--lists LISTS   Change the set of word lists.  This should be a comma-separated
                list of built-in lists (e.g., :code:`--lists=filter,thought`).
                To disable all built-in lists, provide nothing after the
                equals sign (i.e., :code:`--list=`).
--list LIST     Use a custom word list.  The list must be a file that meets
                the worst list format requirements.
--file FILE     Process a file.  This is only necessary if an input file
                matches an argument (e.g., --help).  For files that don't
                share a name with an argument, they should be listed like
                normal.
--stdin         Parse input passed via stdin.  If used with files, the stdin
                input is parsed after all the files.

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
