#!/usr/bin/python3

import operator
import re

import wlint.common
import wlint.punctuation


class PunctuationStyle(wlint.common.Tool):

    def __init__(self):
        super().__init__(description="Check for common punctuation issues")
        self.add_argument(
            "--enable",
            help="Rules to use when processing text.  An asterisk (*) can be "
                 "used for wildcard matching.",
            default="*")
        self.add_argument(
            "--disable",
            help="Rules to disable when processing text.  If a rule is both "
                 "enabled and disabled, disable takes precedence.")

    def setup(self, arguments):
        self.result = 0
        checks = wlint.punctuation.PunctuationRules().rules

        self.checks = {}
        rules = arguments.enable.split(",")
        for rule in rules:
            pattern = re.compile(rule.replace(".", "\.").replace("*", ".*"))
            for (message, fn) in checks:
                if pattern.match(message):
                    self.checks[message] = fn

        if arguments.disable:
            disable = arguments.disable.split(",")
        else:
            disable = []
        for rule in disable:
            if rule:  # don't deal with empty strings
                pattern = re.compile(rule.replace(
                    ".", "\.").replace("*", ".*"))
                rms = []
                for message in self.checks:
                    if pattern.match(message):
                        rms.append(message)
                for message in rms:
                    del self.checks[message]

    def _process(self, file_handle):
        line_number = 0
        hits = []
        for text in file_handle:
            text = self.purify(text)
            line_number += 1
            for (message, fn) in self.checks.items():
                if fn(text, lambda pos:
                        hits.append((line_number, pos, message))):
                    self.result = 1
        return hits

    def process(self, fileHandle):
        hits = sorted(self._process(fileHandle))
        for (line, col, message) in hits:
            print("{}-{}:{} {}".format(fileHandle.name, line, col, message))


punctuationStyle = PunctuationStyle()
wlint.common.execute_tool(punctuationStyle)
