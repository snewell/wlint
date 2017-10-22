#!/usr/bin/python3

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

    def _get_enabled_rules(enabled_rules):
        ret = {}
        rules = enabled_rules.split(",")
        all_rules = wlint.punctuation.get_all_rules()
        for rule in rules:
            pattern = re.compile(rule.replace(".", "\.").replace("*", ".*"))
            for (message, fn) in all_rules:
                if pattern.match(message):
                    ret[message] = fn
        return ret

    def _remove_disabled_rules(self, disabled_rules):
        for rule in disabled_rules:
            if rule:  # don't deal with empty strings
                pattern = re.compile(rule.replace(
                    ".", "\.").replace("*", ".*"))
                rms = []
                for message in self.checks:
                    if pattern.match(message):
                        rms.append(message)
                for message in rms:
                    del self.checks[message]

    def setup(self, arguments):
        self.result = 0
        self.checks = PunctuationStyle._get_enabled_rules(arguments.enable)
        if arguments.disable:
            disable = arguments.disable.split(",")
            self._remove_disabled_rules(disable)

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
