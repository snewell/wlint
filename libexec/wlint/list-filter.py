#!/usr/bin/python3

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

    def setup(self, arguments):
        lists = arguments.lists.split(",")
        # Read the built in lists
        words = defaultLists.buildWordList(lists)

        # Read any extra lists
        for wordList in arguments.list:
            words.addWords(wordList)

        # WordList is complete, so setup variables
        self.filter = wlint.filter.Filter(words)
        self.hits = []
        self.missingFiles = []

    def process(self, fileHandle):
        self.filter.parseHandle(fileHandle,
                                lambda word, line, col: self.hits.append(
                                    (fileHandle.name, word, line, col)))


listFilter = ListFilter()
try:
    listFilter.execute()

    listFilter.hits.sort()
    for (file, word, line, col) in listFilter.hits:
        print("{} {} ({}:{})".format(file, word, line, col))

    if listFilter.missingFiles:
        print(
            "Error opening files: {}".format(
                listFilter.missingFiles),
            file=sys.stderr)
        exit(1)
except ValueError as e:
    print("Error: {}".format(str(e)), file=sys.stderr)
    exit(1)
