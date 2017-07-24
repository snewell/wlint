===========
count-words
===========

----------------------------
count the frequency of words
----------------------------

.. BEGIN_MAN_SECTION

:Author: Stephen Newell
:Copyright: BSD Two-Clause
:Version: 0.1.0
:Manual section: 1
:Manual group: wlint manual

.. END_MAN_SECTION

Synopsis
--------
:code:`count-words [options] [file [file ...]]`


Description
-----------
Each word in the file and its number of occurances will be displayed.  If more
than one file is specified, the full word list and count will be provided
after each file's summary.

::

    sample_input.txt: 18
    a       1       0.05556
    begin   1       0.05556
    day     1       0.05556
    do      1       0.05556
    each    1       0.05556
    feel    1       0.05556
    happy   2       0.11111
    i       1       0.05556
    like    1       0.05556
    nice    1       0.05556
    <trimmed...>


If no files are specified, input is read via standard input.


Options
-------
-h, --help        show this help message and exit
--file FILE       Process a file. This is only necessary if an input file
                  matches an argument (e.g., --help).
--case-sensitive  Treat words differently if they use a different case.
--summarize       Only print summarized results.
--sort-count      Print largest counts first [Default: alphabetize words
                  while printing]
--ignore IGNORE   A comma-separated list of words to skip while processing
                  input.
