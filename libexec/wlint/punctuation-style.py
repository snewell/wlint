#!/usr/bin/python3

import re

import wlint.common

class PunctuationStyle(wlint.common.Tool):
    left_double_quote = "“"
    right_double_quote = "”"

    left_single_quote = "‘"
    right_single_quote = "’"

    thin_sapce_break = " "
    thin_space_nonbreak = " "

    def __init__(self, description):
        super().__init__(description)
        self.checks = {
            "missing space (opening quotes)": re.compile(
                "{}{}".format(
                    PunctuationStyle.left_double_quote,
                    PunctuationStyle.left_single_quote)),
            "missing space (closing quotes)": re.compile(
                "{}{}".format(
                    PunctuationStyle.right_single_quote,
                    PunctuationStyle.right_double_quote))
        }

    def setup(self, arguments):
        self.result = 0

    def process(self, fileHandle):
        lineNumber = 0
        for text in fileHandle:
            lineNumber += 1
            for message, pattern in self.checks.items():
                match = pattern.search(text)
                while match:
                    self.result = 1
                    print(
                        "{}-{}:{} {}".format(fileHandle.name, lineNumber,
                                             match.start(), message))
                    match = pattern.search(text, match.end())

punctuationStyle = PunctuationStyle("Check for common punctuation issues")
punctuationStyle.execute()
exit(punctuationStyle.result)
