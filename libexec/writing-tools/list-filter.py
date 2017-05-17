#!/usr/bin/python3

import argparse
import re
from os import listdir
from os import path
from sys import argv
from sys import stderr

def addWords(path, words):
	with open(path, "r") as inputList:
		for line in inputList:
			word = line[:-1]
			pattern = re.compile("\\b{}\\b".format(word), re.IGNORECASE)
			words[word] = pattern

def parseWordLists(wordLists):
	global path

	words = { }
	listDir = "{}/../../share/writing-tools/filter-lists".format(path.abspath(path.dirname(argv[0])))

	for wordList in wordLists:
		filePath = "{}/{}-words.txt".format(listDir, wordList)
		try:
			addWords(filePath, words)
		except FileNotFoundError:
			# Assuming no built in lists is the exception, not the rule.
			if wordList != "":
				print("Invalid list: {}".format(wordList), file=stderr)
	return words

def readDefaults():
	global path

	listDir = "{}/../../share/writing-tools/filter-lists".format(path.abspath(path.dirname(argv[0])))
	files = listdir(listDir)
	pattern = re.compile("^([a-z]+)-words.txt$")
	ret = [ ]
	for file in files:
		m = pattern.search(file)
		if m:
			ret.append(m.group(1))
	ret.sort()
	return ",".join(ret)

def parseFiles(files, words, missing):
	for f in files:
		try:
			with open(f, 'r') as readFile:
					lineNumber = 0
					for line in readFile:
						lineNumber += 1
						for word, pattern in words.items():
							match = pattern.search(line)
							while match:
								print("{} {} ({}:{})".format(f, word, lineNumber, match.start()))
								match = pattern.search(line, match.end())
		except FileNotFoundError:
			missing.append(f)

defaultWordLists = readDefaults()

parser = argparse.ArgumentParser(description="Detect troublesome words")
parser.add_argument("--lists", help="Change the set of word lists.  This should be a comma-separated list of built-in lists.  [Default={}]".format(defaultWordLists),
                    default=defaultWordLists)
parser.add_argument("--list", help="Use a custom word list.  The list should be a plain text file with one word per line.",
                    action='append', default=[])
parser.add_argument("--file", help="Process a file.  This is only necessary if an input file matches an argument (e.g., --help).",
                    action='append', default=[])
parser.add_argument("files", help="Files to process.", nargs='*', metavar="file")

args = parser.parse_args()
if len(args.files) > 0 or len(args.file) > 0:
	args.lists = args.lists.split(",")

	words = parseWordLists(args.lists)
	for wordList in args.list:
		try:
			addWords(wordList, words)
		except FileNotFoundError:
			print("Invalid list: {}".format(wordList), file=stderr)

	missingFiles = [ ]
	parseFiles(args.files, words, missingFiles)
	parseFiles(args.file, words, missingFiles)

	if len(missingFiles) > 0:
		print("Error opening files: {}".format(missingFiles), file=stderr)
		exit(1)

else:
	print("Error: no files specified ({} -h)".format(argv[0]), file=stderr)
	exit(1)
