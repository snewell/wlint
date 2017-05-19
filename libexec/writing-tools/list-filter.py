#!/usr/bin/python3

import argparse
import re
from os import listdir
from os import path
from wtool import filter
from sys import argv
from sys import stderr

def parseWordLists(path, wordLists):
    """Parse built-in word lists for filtering.

    Arguments:
    path -- the path where built-in strings are stored
    wordLists -- the files to read from path"""
    words = filter.WordList()

    for wordList in wordLists:
        filePath = "{}/{}-words.txt".format(path, wordList)
        try:
            words.addWords(filePath)
        except FileNotFoundError:
            # Assuming no built in lists is the exception, not the rule.
            if wordList != "":
                print("Invalid list: {}".format(wordList), file=stderr)
    return words

def readDefaults(path):
    """Get a list of built-in word lists.

    Arguments:
    path -- the path where built-in strings are stored"""
    files = listdir(path)
    pattern = re.compile("^([a-z]+)-words.txt$")
    ret = [ ]
    for file in files:
        m = pattern.search(file)
        if m:
            ret.append(m.group(1))
    ret.sort()
    return ",".join(ret)

def parseFiles(files, filter, hits, missing):
    """Parse a list of files, searching for filtered words.

    Arguments:
    files -- a list of files to parse (each file should be a full path)
    filter -- a Filter object
    hits -- a list to store filter's matches
    missing -- a list to store entires in files that don't exist"""
    for f in files:
        try:
            filter.parseFile(f, lambda word, line, col: hits.append((f, word, line, col)))
        except FileNotFoundError:
            missing.append(f)

listDir = "{}/../../share/writing-tools/filter-lists".format(path.abspath(path.dirname(argv[0])))
defaultWordLists = readDefaults(listDir)

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

    words = parseWordLists(listDir, args.lists)
    for wordList in args.list:
        try:
            words.addWords(wordList, words)
        except FileNotFoundError:
            print("Invalid list: {}".format(wordList), file=stderr)

    filter = filter.Filter(words)
    hits = [ ]
    missingFiles = [ ]
    parseFiles(args.files, filter, hits, missingFiles)
    parseFiles(args.file, filter, hits, missingFiles)

    for (file, word, line, col) in hits:
        print("{} {} ({}:{})".format(file, word, line, col))

    if len(missingFiles) > 0:
        print("Error opening files: {}".format(missingFiles), file=stderr)
        exit(1)

else:
    print("Error: no files specified ({} -h)".format(argv[0]), file=stderr)
    exit(1)
