#!/usr/bin/python3

import os
import re
import sys

import wlint.common


class WordCounter(wlint.common.Tool):

    def __init__(self):
        super().__init__("Count the occurrence of each word")
        # Is there a way to have \w not match numbers?
        self.pattern = re.compile("\\b([a-zA-Z\\-\\']+)\\b")
        self.add_argument(
            "--case-sensitive",
            help="Treat words differently if they use a different case.",
            action="store_true")

    def setup(self, arguments):
        self.counts = {}

        def case_sensitive(word):
            return word

        def case_insensitive(word):
            return word.lower()

        if arguments.case_sensitive:
            self.key_builder = case_sensitive
        else:
            self.key_builder = case_insensitive

    def process(self, fileHandle):
        localCounts = {}
        for text in fileHandle:
            match = self.pattern.search(text)
            while match:
                word = self.key_builder(match.group(1))
                if word in localCounts:
                    localCounts[word] += 1
                else:
                    localCounts[word] = 1
                match = self.pattern.search(text, match.end())

        if localCounts:
            print("{}:".format(fileHandle.name))
            for word in sorted(localCounts):
                print("{}\t{}".format(word, localCounts[word]))
            print("")


wordCounter = WordCounter()
try:
    wordCounter.execute()
except Exception as e:
    print("Error: {}".format(str(e)), file=sys.stderr)
    exit(1)
