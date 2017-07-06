#!/usr/bin/python3

import operator

import wlint.common
import wlint.punctuation


class PunctuationStyle(wlint.common.Tool):

    def __init__(self, description):
        super().__init__(description)
        self.checks = wlint.punctuation.PunctuationRules().rules

    def setup(self, arguments):
        self.result = 0

    def process(self, fileHandle):
        lineNumber = 0
        hits = []
        for text in fileHandle:
            lineNumber += 1
            for message, fn in self.checks.items():
                if fn(text, lambda pos: hits.append(lineNumber, pos, message)):
                    self.result = 1

        hits.sort()
        for (line, col, message) in hits:
            print("{}-{}:{} {}".format(fileHandle.name, line, pos, message))


punctuationStyle = PunctuationStyle("Check for common punctuation issues")
punctuationStyle.execute()
exit(punctuationStyle.result)
