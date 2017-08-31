#!/usr/bin/python3

import operator
import re
import sys

import wlint.common


def print_counts(counts, total_words):
    for word, count in counts:
        ratio = count / total_words
        print("{}\t{}\t{:.5f}".format(word, count, ratio))


class WordCounter(wlint.common.Tool):

    def __init__(self):
        super().__init__("Count the occurrence of each word")
        # Is there a way to have \w not match numbers?
        self.pattern = re.compile(r"\b([\w\-\']+)\b")
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
        self.add_argument(
            "--ignore",
            help="A comma-separated list of words to skip while processing "
                 "input.",
            default="")

    def setup(self, arguments):
        self.counts = {}
        self.file_count = 0
        self.total_words = 0

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

        self.ignore = {}
        ignore = arguments.ignore.split(",")
        for word in ignore:
            self.ignore[word] = None

    def process(self, fileHandle):
        localCounts = {}

        def update_counts(word, counts):
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

        file_words = 0
        for text in fileHandle:
            text = self.purify(text)
            match = self.pattern.search(text)
            while match:
                word = self.key_builder(match.group(1))
                if word not in self.ignore:
                    update_counts(word, localCounts)
                    update_counts(word, self.counts)
                    file_words += 1
                match = self.pattern.search(text, match.end())

        self.total_words += file_words
        if localCounts:
            if not self.summarize_only:
                print("{}: {}".format(fileHandle.name, file_words))
                print_counts(self.get_counts(localCounts), file_words)
                print("")
            self.file_count += 1

    def get_counts(self, counts):
        list_items = list(counts.items())
        if self.sort_count:
            list_items.sort(key=operator.itemgetter(0))
            list_items.sort(key=operator.itemgetter(1), reverse=True)
        else:
            list_items.sort()
        return list_items

    def display_results(self):
        if self.file_count > 1:
            print("Total: {}".format(self.total_words))
            print_counts(self.get_counts(self.counts), self.total_words)


wordCounter = WordCounter()
wlint.common.execute_tool(wordCounter)
