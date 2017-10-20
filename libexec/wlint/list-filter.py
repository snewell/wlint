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
                 "comma-separated list of built-in lists.",
            default=defaultListsStr)
        self.add_argument(
            "--list",
            help="Use a custom word list.  The list should be a plain text "
                 "file with one word per line.",
            action="append")

        self.add_sort(["alpha", "sequential"])
        self.sort_fns = {
            "alpha": lambda hits: hits.sort(),
            "sequential": lambda hits: hits.sort(key=operator.itemgetter(1, 2))
        }

    def setup(self, arguments):
        def make_lists():
            if arguments.lists:
                lists = arguments.lists.split(",")
                # Read the built in lists
                return defaultLists.buildWordList(lists)
            else:
                return wlint.filter.WordList()

        words = make_lists()
        # Read any extra lists
        if arguments.list:
            for wordList in arguments.list:
                words.addWords(wordList)

        # WordList is complete, so setup variables
        self.filter = wlint.filter.Filter(words, self.purifier)
        self.missingFiles = []

        self.sorter = self.sort_fns[self.sort]

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
wlint.common.execute_tool(listFilter)
