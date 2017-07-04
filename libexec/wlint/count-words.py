#!/usr/bin/python3

import operator
import re
import sys

import wlint.common


def print_counts(counts):
    for word, count in counts:
        print("{}\t{}".format(word, count))


class WordCounter(wlint.common.Tool):

    def __init__(self):
        super().__init__("Count the occurrence of each word")
        # Is there a way to have \w not match numbers?
        self.pattern = re.compile("\\b([a-zA-Z\\-\\']+)\\b")
        self.add_argument(
            "--case-sensitive",
            help="Treat words differently if they use a different case.",
            action="store_true")
        self.add_argument(
            "--summarize",
            help="Only print summarized results.",
            action="store_true")
        self.add_argument(
            "--sort-count",
            help="Print largest counts first [Default: alphabetize words "
            "while printing]",
            action="store_true")

    def setup(self, arguments):
        self.counts = {}
        self.file_count = 0

        def case_sensitive(word):
            return word

        def case_insensitive(word):
            return word.lower()

        if arguments.case_sensitive:
            self.key_builder = case_sensitive
        else:
            self.key_builder = case_insensitive

        self.summarize_only = arguments.summarize
        self.sort_count = arguments.sort_count

    def process(self, fileHandle):
        localCounts = {}

        def update_counts(word, counts):
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

        for text in fileHandle:
            match = self.pattern.search(text)
            while match:
                word = self.key_builder(match.group(1))
                update_counts(word, localCounts)
                update_counts(word, self.counts)
                match = self.pattern.search(text, match.end())

        if localCounts:
            if not self.summarize_only:
                print("{}:".format(fileHandle.name))
                print_counts(self.get_counts(localCounts))
                print("")
            self.file_count += 1

    def get_counts(self, counts):
        list_items = list(counts.items())
        if self.sort_count:
            list_items.sort(key=operator.itemgetter(1, 0), reverse=True)
        else:
            list_items.sort()
        return list_items


wordCounter = WordCounter()
try:
    wordCounter.execute()
    if wordCounter.file_count > 1:
        print("Total:")
        print_counts(wordCounter.get_counts(wordCounter.counts))
except Exception as e:
    print("Error: {}".format(str(e)), file=sys.stderr)
    exit(1)
