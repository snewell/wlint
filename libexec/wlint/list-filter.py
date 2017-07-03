#!/usr/bin/python3

import operator
import os
import sys

import wlint.common
import wlint.filter

listDir = "{}/../../share/wlint/filter-lists" \
    .format(os.path.abspath(os.path.dirname(sys.argv[0])))
defaultLists = wlint.filter.DirectoryLists(listDir)


class ListFilter(wlint.common.Tool):

    def __init__(self):
        super().__init__(description="Detect troublesome words")
        defaultListsStr = ",".join(defaultLists.files)
        self.add_argument(
            "--lists",
            help="Change the set of word lists.  This should be a "
                 "comma-separated list of built-in lists.  [Default={}]"
                 .format(defaultListsStr),
            default=defaultListsStr)
        self.add_argument(
            "--list",
            help="Use a custom word list.  The list should be a plain text "
                 "file with one word per line.",
            action="append",
            default=[])
        self.add_argument(
            "--sort-method",
            help="Method to sort discovered words.  Options are alpha (filter"
            " words are alphabetized and grouped) and sequential (the order "
            "words appear in input).  The default is alpha.",
            default="alpha")

    def setup(self, arguments):
        lists = arguments.lists.split(",")
        # Read the built in lists
        words = defaultLists.buildWordList(lists)

        # Read any extra lists
        for wordList in arguments.list:
            words.addWords(wordList)

        # WordList is complete, so setup variables
        self.filter = wlint.filter.Filter(words)
        self.missingFiles = []

        def alpha_sort(hits):
            hits.sort()

        def sequential_sort(hits):
            hits.sort(key=operator.itemgetter(1, 2))

        if arguments.sort_method == "alpha":
            self.sorter = alpha_sort
        elif arguments.sort_method == "sequential":
            self.sorter = sequential_sort
        else:
            raise ValueError(
                "'{}' is not a valid sort option".format(
                    arguments.sort_method))

    def process(self, fileHandle):
        hits = []
        self.filter.parseHandle(fileHandle,
                                lambda word, line, col: hits.append(
                                    (word, line, col)))
        self.print_hits(
            hits,
            lambda word,
            line,
            col: print(
                "{} {} ({}:{})".format(
                    fileHandle.name,
                    word,
                    line,
                    col)))

    def print_hits(self, hits, fn):
        self.sorter(hits)
        for (word, line, col) in hits:
            fn(word, line, col)


listFilter = ListFilter()
try:
    listFilter.execute()

    if listFilter.missingFiles:
        print(
            "Error opening files: {}".format(
                listFilter.missingFiles),
            file=sys.stderr)
        exit(1)
except ValueError as e:
    print("Error: {}".format(str(e)), file=sys.stderr)
    exit(1)
