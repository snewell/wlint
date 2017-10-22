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

    def _remove_disabled_rules(disabled_rules, checks):
        for rule in disabled_rules:
            if rule:  # don't deal with empty strings
                pattern = re.compile(rule.replace(
                    ".", "\.").replace("*", ".*"))
                rms = []
                for message in checks:
                    if pattern.match(message):
                        rms.append(message)
                for message in rms:
                    del checks[message]

        return checks

    def setup(self, arguments):
        self.result = 0
        checks = PunctuationStyle._get_enabled_rules(arguments.enable)
        if arguments.disable:
            disable = arguments.disable.split(",")
            checks = PunctuationStyle._remove_disabled_rules(disable, checks)

        self.checks = []
        for (message, fn) in checks.items():
            self.checks.append((message, fn))

    def _process(self, file_handle):
        hits = []
        wlint.punctuation.check_handle(self.checks, file_handle,
                                       lambda line_number, message, pos: hits.append((line_number, pos, message)), self.purify)
        return hits

    def process(self, fileHandle):
        hits = sorted(self._process(fileHandle))
        for (line, col, message) in hits:
            print("{}-{}:{} {}".format(fileHandle.name, line, col, message))


punctuationStyle = PunctuationStyle()
wlint.common.execute_tool(punctuationStyle)
