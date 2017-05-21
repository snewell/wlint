#!/usr/bin/python3

import argparse
from os import path
from sys import argv
from sys import stderr
from sys import stdin

from wtool import filter

listDir = "{}/../../share/wtool/filter-lists" \
            .format(path.abspath(path.dirname(argv[0])))
defaultLists = filter.DirectoryLists(listDir)

defaultListsStr = ",".join(defaultLists.files)
parser = argparse.ArgumentParser(description="Detect troublesome words")
parser.add_argument("--lists", help="Change the set of word lists.  This "
                                    "should be a comma-separated list of "
                                    "built-in lists.  [Default={}]" \
                                        .format(defaultListsStr),
                    default=defaultListsStr)
parser.add_argument("--list", help="Use a custom word list.  The list should "
                                   "be a plain text file with one word per "
                                   "line.",
                    action="append", default=[])
parser.add_argument("--file", help="Process a file.  This is only necessary "
                                   "if an input file matches an argument "
                                   "(e.g., --help).",
                    action="append", default=[])
parser.add_argument("--stdin", help="Parse stdin for filter words.  If both "
                                    "files and this option are used, files "
                                    "are processed before stdin.",
                    action="store_true")
parser.add_argument("files", help="Files to process.", nargs="*",
                    metavar="file")

args = parser.parse_args()
if args.files or args.file or args.stdin:
    args.lists = args.lists.split(",")

    def handleError(e):
        """Print an error message and exit the program.

        Arguments:
        e -- the error that caused the problem"""
        print("Error: {}".format(str(e)))
        exit(1)

    try:
        # Read the built in lists
        words = defaultLists.buildWordList(args.lists)

        # Read any extra lists
        for wordList in args.list:
            words.addWords(wordList)

        # WordList is complete, so setup variables
        filter = filter.Filter(words)
        hits = [ ]
        missingFiles = [ ]

        def parseFiles(files):
            """Parse a list of files, searching for filtered words.

            Arguments:
            files -- a list of files to parse (each file should be a
                     full path)"""
            fn = lambda word, line, col: hits.append((f, word, line, col))
            for f in files:
                try:
                    filter.parseFile(f, fn)
                except FileNotFoundError:
                    missingFiles.append(f)

        # parse normal files, plus anything that was passed in via the
        # "--file" option
        parseFiles(args.files)
        parseFiles(args.file)

        if args.stdin:
            # if we're reading from stdin, we need a slightly different
            # function
            def parseStdin():
                """Read data from stdin that should be searched for filter
                words."""
                lineNumber = 0
                fn = lambda word, col: hits.append(("<stdin>", word,
                                                    lineNumber, col))
                for line in stdin:
                    lineNumber += 1
                    filter.parseLine(line, fn)
            parseStdin()

        # done processing, so sort results before printing them
        hits.sort()
        for (file, word, line, col) in hits:
            print("{} {} ({}:{})".format(file, word, line, col))

        # sort an dprint any missing files to stderr
        missingFiles.sort()
        if missingFiles:
            print("Error opening files: {}".format(missingFiles), file=stderr)
            exit(1)

    except ValueError as e:
        # Invalid built-in list
        handleError(e)
    except FileNotFoundError as e:
        # Invalid extra list
        handleError(e)

else:
    print("Error: no files specified ({} -h)".format(argv[0]), file=stderr)
    exit(1)
