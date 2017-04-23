#!/usr/bin/python3

import re
from os import path
from sys import argv

wordLists = {"thought", "filter", "weasel"}
words = { }

listDir = "{}/../../share/writing-tools/filter-lists".format(path.abspath(path.dirname(argv[0])))

for wordList in wordLists:
    path = "{}/{}-words.txt".format(listDir, wordList)
    with open(path, "r") as inputList:
        for line in inputList:
            word = line[:-1]
            pattern = re.compile("\\b{}\\b".format(word), re.IGNORECASE)
            words[word] = pattern

argv.pop(0)
for arg in argv:
    with open(arg, 'r') as readFile:
        lineNumber = 0
        for line in readFile:
            lineNumber += 1
            for word, pattern in words.items():
                match = pattern.search(line)
                while match:
                    print("{} {} ({}:{})".format(arg, word, lineNumber, match.start()))
                    match = pattern.search(line, match.end())
