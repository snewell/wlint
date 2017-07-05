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

        def regex_rule(pattern_text):
            pattern = re.compile(pattern_text)

            def execute(text, fn):
                hit = False
                match = pattern.search(text)
                while match:
                    hit = True
                    fn(match.start())
                    match = pattern.search(text, match.end())
                return hit

            return execute

        def quote_order_rule(first, second):
            return regex_rule("{}{}".format(first, second))

        def correct_space(first, second):
            predicate = regex_rule("{}\s{}".format(first, second))

            def execute(text, fn):
                hit = False

                def check_pos(pos):
                    if text[pos + 1] != PunctuationStyle.thin_space_nonbreak:
                        fn(pos)
                        hit = True

                predicate(text, check_pos)
                return hit

            return execute

        self.checks = {
            "missing space (opening quotes)": quote_order_rule(
                PunctuationStyle.left_double_quote,
                PunctuationStyle.left_single_quote),
            "missing space (closing quotes)": quote_order_rule(
                PunctuationStyle.right_single_quote,
                PunctuationStyle.right_double_quote),
            "space between opening quotes is not a non-breaking thin space": correct_space(
                PunctuationStyle.left_double_quote,
                PunctuationStyle.left_single_quote),
            "space between closing quotes is not a non-breaking thin space": correct_space(
                PunctuationStyle.right_single_quote,
                PunctuationStyle.right_double_quote)}

    def setup(self, arguments):
        self.result = 0

    def process(self, fileHandle):
        lineNumber = 0
        for text in fileHandle:
            lineNumber += 1
            for message, fn in self.checks.items():
                if fn(text, lambda pos: print(
                    "{}-{}:{} {}".format(fileHandle.name, lineNumber,
                                         pos, message))):
                    self.result = 1


punctuationStyle = PunctuationStyle("Check for common punctuation issues")
punctuationStyle.execute()
exit(punctuationStyle.result)
