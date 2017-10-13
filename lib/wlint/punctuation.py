#!/usr/bin/python3

import re


def _regex_rule(pattern_text):
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


def _pair_regex(first, second):
    return _regex_rule("{}{}".format(first, second))


class PunctuationRules:
    left_double_quote = "“"
    right_double_quote = "”"

    left_single_quote = "‘"
    right_single_quote = "’"

    thin_sapce_break = " "
    thin_space_nonbreak = " "

    emdash = "—"
    endash = "–"

    def _quote_order_rule(self, name, single, double):
        self.rules.append((
            "quotation.missing-space-{}-single-double".format(name),
            _pair_regex(single, double)))
        self.rules.append((
            "quotation.missing-space-{}-double-single".format(name),
            _pair_regex(double, single)))

    def _double_punctuation_rule(self, name, quote):
        self.rules.append((
            "quotation.consecutive-{}-quotes".format(name),
            _pair_regex(quote, quote)))

    def _correct_space_rule(self, name, single, double):
        def correct_space_builder(first, second):
            predicate = _regex_rule("{}\\s{}".format(first, second))

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

        self.rules.append((
            "quotation.incorrect-space-{}-single-double".format(name),
            correct_space_builder(single, double)))
        self.rules.append((
            "quotation.incorrect-space-{}-double-single".format(name),
            correct_space_builder(double, single)))

    def _add_quote_rules(self):
        self._quote_order_rule("opening",
                               PunctuationRules.left_single_quote,
                               PunctuationRules.left_double_quote)
        self._quote_order_rule("closing",
                               PunctuationRules.right_single_quote,
                               PunctuationRules.right_double_quote)

        self._double_punctuation_rule("opening",
                                      PunctuationRules.left_single_quote)
        self._double_punctuation_rule("closing",
                                      PunctuationRules.right_double_quote)

        self._correct_space_rule("opening",
                                 PunctuationRules.left_single_quote,
                                 PunctuationRules.left_double_quote)
        self._correct_space_rule("closing",
                                 PunctuationRules.right_single_quote,
                                 PunctuationRules.right_double_quote)

    def _colon_rule(self, name, colon):
        # a colon might be followed by a digit if it's time
        if name == "colon":
            self.rules.append(("{}.missing-space".format(name),
                               _pair_regex(colon, "[^\\s\\d]")))
        elif name == "semicolon":
            self.rules.append(("{}.missing-space".format(name),
                               _pair_regex(colon, "\\S")))

        self.rules.append(("{}.preceeding-space".format(name),
                           _pair_regex("\\s", colon)))

    def _add_colon_rules(self):
        self.rules.append(("emdash.replace-double-hyphen",
                           _regex_rule("\\-\\-")))
        self.rules.append(("emdash.preceeding-space",
                           _pair_regex("\\s", PunctuationRules.emdash)))
        self.rules.append(("emdash.trailing-space",
                           _pair_regex(PunctuationRules.emdash, "\\s")))

        self._colon_rule("colon", ":")
        self._colon_rule("semicolon", ";")

    def _uppercase_ampm_builder(self, time_regex_with_space):
        def builder(first, second):
            ampm_regex_uppercase = "(?:[{}]\\.?{}\\.?)".format(first,
                                                               second)
            self.rules.append(("time.uppercase-{}{}".format(first, second),
                               _pair_regex(time_regex_with_space,
                                           ampm_regex_uppercase)))

        builder("AP", "m")
        builder("AP", "M")
        builder("ap", "M")

    def _add_time_rules(self):
        time_regex = "(?:1[0-2]|0?[1-9]):(?:[0-5][0-9])"
        time_regex_with_space = "(?:1[0-2]|0?[1-9]):(?:[0-5][0-9] ?)"
        ampm_regex = "(?:[AaPp]\\.?[Mm]\\.?)"
        ampm_regex_no_periods = "(?:[AaPp][Mm])"

        self.rules.append(("time.missing-periods",
                           _pair_regex(time_regex_with_space,
                                       ampm_regex_no_periods)))
        self.rules.append(("time.missing-space",
                           _pair_regex(time_regex, ampm_regex)))
        self._uppercase_ampm_builder(time_regex_with_space)

    def _range_rule(self, pattern):
        self.rules.append(("endash.preceeding-space",
                           _regex_rule("{}\\s+{}\\s*{}".format(
                               pattern, PunctuationRules.endash,
                               pattern))))
        self.rules.append(("endash.trailing-space",
                           _regex_rule("{}\\s*{}\\s+{}".format(
                               pattern, PunctuationRules.endash,
                               pattern))))

        self.rules.append(("endash.replace-hyphen",
                           _regex_rule("{}\\s*-\\s*{}".format(
                               pattern, pattern))))
        self.rules.append(("endash.replace-emdash",
                           _regex_rule("{}\\s*{}\\s*{}".format(
                               pattern, PunctuationRules.emdash,
                               pattern))))

    def __init__(self):
        self.rules = []
        self._add_quote_rules()
        self._add_colon_rules()
        self._add_time_rules()

        self._range_rule("\\d+")
