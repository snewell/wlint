#!/usr/bin/python3

import re


class PunctuationRules:
    left_double_quote = "“"
    right_double_quote = "”"

    left_single_quote = "‘"
    right_single_quote = "’"

    thin_sapce_break = " "
    thin_space_nonbreak = " "

    def __init__(self):
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

        def pair_regex(first, second):
            return regex_rule("{}{}".format(first, second))

        def quote_order_rule(name, single, double):
            self.rules[
                "quotation.missing-{}-space-single-double".format(name)] = pair_regex(single, double)
            self.rules[
                "quotation.missing-{}-space-double-single".format(name)] = pair_regex(double, single)

        def double_punctuation_rule(name, quote):
            self.rules[
                "quotation.consecutive-{}-quotes".format(name)] = pair_regex(quote, quote)

        def correct_space_rule(name, single, double):
            def correct_space_builder(first, second):
                predicate = regex_rule("{}\\s{}".format(first, second))

                def execute(text, fn):
                    hit = False

                    def check_pos(pos):
                        if text[
                                pos +
                                1] != PunctuationRules.thin_space_nonbreak:
                            fn(pos)
                            hit = True

                    predicate(text, check_pos)
                    return hit

                return execute

            self.rules[
                "quotation.incorrect-space-{}-single-double".format(name)] = correct_space_builder(single, double)
            self.rules[
                "quotation.incorrect-space-{}-double-single".format(name)] = correct_space_builder(double, single)

        self.rules = {}

        quote_order_rule("opening",
                         PunctuationRules.left_single_quote,
                         PunctuationRules.left_double_quote)
        quote_order_rule("closing",
                         PunctuationRules.right_single_quote,
                         PunctuationRules.right_double_quote)
        double_punctuation_rule("opening", PunctuationRules.left_single_quote)
        double_punctuation_rule("closing", PunctuationRules.right_double_quote)
        correct_space_rule("opening",
                           PunctuationRules.left_single_quote,
                           PunctuationRules.left_double_quote)
        correct_space_rule("closing",
                           PunctuationRules.right_single_quote,
                           PunctuationRules.right_double_quote)

