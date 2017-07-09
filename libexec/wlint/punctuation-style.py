#!/usr/bin/python3

import operator

import wlint.common
import wlint.punctuation


class PunctuationStyle(wlint.common.Tool):

    def __init__(self):
        super().__init__("Check for common punctuation issues")
        self.checks = wlint.punctuation.PunctuationRules().rules

    def setup(self, arguments):
        self.result = 0

    def process(self, fileHandle):
        lineNumber = 0
        hits = []
        for text in fileHandle:
            lineNumber += 1
            for (message, fn) in self.checks:
                if fn(
                    text, lambda pos: hits.append(
                        (lineNumber, pos, message))):
                    self.result = 1

        hits.sort()
        for (line, col, message) in hits:
            print("{}-{}:{} {}".format(fileHandle.name, line, col, message))


punctuationStyle = PunctuationStyle()
wlint.common.execute_tool(punctuationStyle)
