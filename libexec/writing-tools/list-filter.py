#!/usr/bin/python3

import re
from os import listdir
from os import path
from sys import argv
from sys import stderr

def printHelp(name, defaultLists):
    name = path.basename(name)
    print("{} - Detect troublesome words".format(name))
    print("{} [options] <file1> [<file2> ...]".format(name))
    print("\nOPTIONS")
    print("  --help, -h       Display this help message and exit")
    print("  --lists=<lists>  Change the set of word lists.  <lists> should be a")
    print("                   comma-separated list of *builit-in* lists to use.")
    print("                   [Default: {}]".format(", ".join(str(l) for l in defaultLists)))
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
    return ret

# default word lists
defaultWordLists = readDefaults()

if len(argv) > 1:
    wordLists = defaultWordLists
    extraLists = [ ]

    index = 1
    # parse optoins
    while index < len(argv):
        if argv[index] == "--help":
            printHelp(argv[0], defaultWordLists)
            exit(0)
        elif argv[index] == "-h":
            printHelp(argv[0], defaultWordLists)
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

    missingFiles = [ ]
    # We should only have files at this point
    while index < len(argv):
        try:
            with open(argv[index], 'r') as readFile:
                lineNumber = 0
                for line in readFile:
                    lineNumber += 1
                    for word, pattern in words.items():
                        match = pattern.search(line)
                        while match:
                            print("{} {} ({}:{})".format(argv[index], word, lineNumber, match.start()))
                            match = pattern.search(line, match.end())
        except FileNotFoundError:
            missingFiles.append(argv[index])
        index += 1

    if len(missingFiles) > 0:
        print("Error opening files: {}".format(missingFiles), file=stderr)
        exit(1)
else:
    printHelp(argv[0], defaultWordLists)
