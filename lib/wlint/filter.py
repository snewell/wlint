#!/usr/bin/python3

import os
import re


class WordList:

    """A list of words to search for"""

    def __init__(self):
        self.words = {}

    def addWord(self, word):
        """Add a word to the list.

        Arguments:
        word -- the word to add"""
        pattern = re.compile("\\b{}\\b".format(word), re.IGNORECASE)
        self.words[word] = pattern

    def addWords(self, path):
        """Add words from a file.  Each entry should be on a new line
        and is treated as the literal entry.

        Arguments:
        path -- path of the file to parse"""
        with open(path, "r") as inputList:
            for line in inputList:
                self.addWord(line[:-1])


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

    def buildWordList(self, wordLists):
        """Parse built-in word lists for filtering.

        Arguments:
        wordLists -- the subset of built-in lists to use"""
        words = WordList()

        for wordList in wordLists:
            filePath = "{}/{}-words.txt".format(self.path, wordList)
            try:
                words.addWords(filePath)
            except FileNotFoundError:
                raise \
                    ValueError("'{}' is not a built in list".format(wordList))
        return words


class Filter:

    """An object to filter files."""

    def __init__(self, words):
        """Construct a Filter.

        Arguments:
        words -- the WordList to use"""
        self.words = words

    def parseLine(self, line, fn):
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

    def parseFile(self, path, fn):
        """Parse a file.

        Arguments:
        path -- the file to parse
        fn -- A function to invoke on each match.  Arguments are: word,
              lineNumber, column."""
        with open(path, 'r') as readFile:
            line = 0
            for text in readFile:
                line += 1
                self.parseLine(text, lambda word, col: fn(word, line, col))
