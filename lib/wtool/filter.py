#!/usr/bin/python3

import argparse
import re

class WordList:
	def __init__(self):
		self.words = { }

	def addWord(self, word):
		pattern = re.compile("\\b{}\\b".format(word), re.IGNORECASE)
		self.words[word] = pattern

class Filter:
	def __init__(self, words):
		self.words = words

	def parseFile(self, path, fn):
		with open(path, 'r') as readFile:
			lineNumber = 0
			for line in readFile:
				lineNumber += 1
				for word, pattern in self.words.words.items():
					match = pattern.search(line)
					while match:
						fn(path, word, lineNumber, match.start())
						match = pattern.search(line, match.end())
