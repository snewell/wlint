#!/usr/bin/python3

import argparse
import re

class WordList:
    """A list of words to search for"""
    def __init__(self):
        self.words = { }

    def addWord(self, word):
        """Add a word to the list.

        Arguments:
        word -- the word to add"""
        pattern = re.compile("\\b{}\\b".format(word), re.IGNORECASE)
        self.words[word] = pattern

    def addWords(self, path):
        """Add words from a file.  Each entry should be on a new line and is
        treated as the literal entry.

        Arguments:
        path -- path of the file to parse"""
        with open(path, "r") as inputList:
            for line in inputList:
                self.addWord(line[:-1])

class Filter:
    """An object to filter files."""
    def __init__(self, words):
        """Construct a Filter.

        Arguments:
        words -- the WordList to use"""
        self.words = words

    def parseFile(self, path, fn):
        """Parse a file.

        Arguments:
        path -- the file to parse
        fn -- A function to invoke on each match.  Arguments are: word, lineNumber, column."""
        with open(path, 'r') as readFile:
            lineNumber = 0
            for line in readFile:
                lineNumber += 1
                for word, pattern in self.words.words.items():
                    match = pattern.search(line)
                    while match:
                        fn(word, lineNumber, match.start())
                        match = pattern.search(line, match.end())
