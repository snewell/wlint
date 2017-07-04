punctuation-style
=================
punctuation-style is a tool to check for common punctutaion issues.

Usage
-----
:code:`punctuation-style [options] file [file ...]`

Any punctuation style issues detected will be displayed with line and column
offsets.

::

    wolf.txt-3533:47 missing space (opening quotes)
    wolf.txt-4129:44 missing space (opening quotes)
    wolf.txt-4136:0 missing space (opening quotes)
    wolf.txt-5521:23 missing space (closing quotes)

If no files are specified, input is read via standard input.

Options
-------
-h, --help        show this help message and exit
--file FILE       Process a file. This is only necessary if an input file
                  matches an argument (e.g., --help).
