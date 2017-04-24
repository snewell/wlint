#!/usr/bin/python3

import re
from os import path
from sys import argv

def printHelp(name):
    name = path.basename(name)
    print("{} - Detect troublesome words".format(name))
    print("{} [options] <file1> [<file2> ...]".format(name))
    print("\nOPTIONS")
    print("  --help, -h       Display this help message")
    print("  --lists=<lists>  Change the set of word lists.  <lists> should be a")
    print("                   comma-separated list of *builit-in* options to use.")
    print("                   [Default: filter, thought, weasel]")
    print("  --list=<list>    Use a custom word list.  <list> should be a path to a text")
    print("                   file with one word per line.")
    print("  --               Stop processing options (required if files to parse match")
    print("                   any of these options)")
    print("\nEXAMPLES")
    print("  {} foo.txt".format(name))
    print("  {} foo.txt bar.txt".format(name))
    print("  {} --lists=filter,weasel foo.txt".format(name))
    print("  {} --list=my_list.txt foo.txt".format(name))
    print("  {} --list=my_list.txt --list=another_list.txt foo.txt".format(name))
    print("  {} --lists=filter --list=mylist.txt foo.txt".format(name))

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
        addWords(filePath, words)
    return words

if len(argv) > 1:
    # default word lists
    wordLists = ["thought", "filter", "weasel"]
    extraLists = [ ]

    index = 1
    # parse optoins
    while index < len(argv):
        if argv[index] == "--help":
            printHelp(argv[0])
            exit(0)
        elif argv[index] == "-h":
            printHelp(argv[0])
            exit(0)
        elif argv[index] == "--":
            break
        elif re.match("^--lists=", argv[index]):
            newList = argv[index].split('=')[1]
            if len(newList) > 0:
                wordLists = newList.split(",")
            else:
                wordLists = []
        elif re.match("^--list=", argv[index]):
            extraLists.append(argv[index].split('=')[1])
        else:
            # not an option
            break
        index += 1

    words = parseWordLists(wordLists)
    for wordList in extraLists:
        addWords(wordList, words)

    # We should only have files at this point
    while index < len(argv):
        with open(argv[index], 'r') as readFile:
            lineNumber = 0
            for line in readFile:
                lineNumber += 1
                for word, pattern in words.items():
                    match = pattern.search(line)
                    while match:
                        print("{} {} ({}:{})".format(argv[index], word, lineNumber, match.start()))
                        match = pattern.search(line, match.end())
        index += 1
else:
    printHelp(argv[0])
