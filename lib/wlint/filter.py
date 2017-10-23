#!/usr/bin/python3

import os
import re

import wlint.purify


class WordList:

    """A list of words to search for"""

    def __init__(self):
        self.words = {}

    def add_word(self, word):
        """Add a word to the list.

        Arguments:
        word -- the word to add"""
        pattern = re.compile(r"\b{}\b".format(word), re.IGNORECASE)
        self.words[word] = pattern

    def add_word_sequence(self, sequence, purifier=None):
        """Add a series of words to the word list.

        Arguments:
        sequence -- some object that can be iterated over.
        purifier -- A function to run on each item in sequence.  This isn't
                    needed in most cases, but can be useful if sequence is
                    something like a file (you wouldn't want the newlines)."""
        if not purifier:
            purifier = wlint.purify.text

        for word in sequence:
            self.add_word(purifier(word))


class DirectoryLists:

    """A collection of lists in a directory."""

    def __init__(self, path):
        """Constrcut a directory list.

        Arguments:
        path -- path to the directory"""
        self.path = path
        files = os.listdir(path)
        pattern = re.compile("^([a-z]+)-words.txt$")
        self.files = []
        for file in files:
            m = pattern.search(file)
            if m:
                self.files.append(m.group(1))
        self.files.sort()

    def buildWordList(self, word_lists):
        """Parse built-in word lists for filtering.

        Arguments:
        word_lists -- the subset of built-in lists to use"""
        words = WordList()

        for word_list in word_lists:
            file_path = "{}/{}-words.txt".format(self.path, word_list)
            try:
                with open(file_path, "r") as input_list:
                    words.add_word_sequence(input_list, lambda t: t[:-1])
            except FileNotFoundError:
                raise \
                    ValueError("'{}' is not a word list".format(file_path))
        return words


class Filter:

    """An object to filter files."""

    def __init__(self, words):
        """Construct a Filter.

        Arguments:
        words -- the WordList to use"""
        self.words = words

    def filter_line(self, line, fn):
        """Search one line of text for any filter words.

        Arguments:
        line -- the line of text to parse
        fn -- The function to call when a filter word is found.  Arguments are
              word, lineNumber."""
        for word, pattern in self.words.words.items():
            match = pattern.search(line)
            while match:
                fn(word, match.start())
                match = pattern.search(line, match.end())

    def filter_sequence(self, sequence, fn, purifier=None):
        """Parse a sequence.

        Arguments:
        sequence -- an iterable object to filter over
        fn -- A function to invoke on each match.  Arguments are: word,
              lineNumber, column.
        purifier -- A function to purify each line of text.  If not provided,
                    the text will not be modified."""
        if not purifier:
            purifier = wlint.purify.text

        line = 0
        for text in sequence:
            line += 1
            self.filter_line(purifier(text), lambda word,
                             col: fn(word, line, col))
