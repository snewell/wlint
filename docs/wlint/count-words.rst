count-words
===========
count-words is a tool to count the frequency of each word in a set of files.

Usage
-----
:code:`count-wrods [options] file [file ...]`

Each word in the file and its number of occurances will be displayed.  If more
than one file is specified, the full word list and count will be provided
after each file's summary.

::

    sample-input.txt:
    a       16
    accomplice      1
    after   1
    again   1
    against 3
    ago     1
    ain't   4
    all     4
    am      1

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
