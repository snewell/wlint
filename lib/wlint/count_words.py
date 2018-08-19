#!/usr/bin/python3

import operator

import wlint.common
import wlint.wordcounter


def print_counts(counts, total_words):
    for word, count in counts:
        ratio = count / total_words
        print("{}\t{}\t{:.5f}".format(word, count, ratio))


class WordCounter(wlint.common.Tool):

    def __init__(self):
        super().__init__(description="Count the occurrence of each word")
        # Is there a way to have \w not match numbers?
        # We're going to a call a word anything with these properties:
        #  - surrounded by word boundaries (\b)
        #  - 1 or more:
        #    - word characters
        #    - hyphens
        #    - single quotes (for "plain text" apostrophes)
        #    - right single quotes (for "smart" apostrophes)
        self.add_argument(
            "--case-sensitive",
            help="Treat words differently if they use a different case.",
            action="store_true")
        self.add_argument(
            "--summarize",
            help="Only print summarized results.",
            action="store_true")
        self.add_argument(
            "--ignore",
            help="A comma-separated list of words to skip while processing "
                 "input.")

        self.add_sort(["alpha", "count"])

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
        self.sort_count = self.sort == "count"

        self.ignore = {}
        if arguments.ignore:
            ignore = arguments.ignore.split(",")
            for word in ignore:
                self.ignore[word] = None

    def _count_words(self, file_handle):
        file_counts = wlint.wordcounter.count_handle(
            file_handle, lambda t: self.key_builder(self.purify(t)))

        for word in self.ignore:
            if word in file_counts[0]:
                file_counts[1] -= file_counts[0][word]
                del file_counts[0][word]

        return file_counts

    def process(self, fileHandle):
        current_file_counts = self._count_words(fileHandle)

        self.total_words += current_file_counts[1]
        if current_file_counts[0]:
            if not self.summarize_only:
                print("{}: {}".format(fileHandle.name, current_file_counts[1]))
                print_counts(self.get_counts(current_file_counts[0]),
                             current_file_counts[1])
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


def main(args=None):
    wordCounter = WordCounter()
    wlint.common.execute_tool(wordCounter, args)


_COUNT_WORDS_COMMAND = (
    main,
    "Count words")

if __name__ == '__main__':
    main()
