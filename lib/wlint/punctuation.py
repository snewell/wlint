#!/usr/bin/python3

import re

import wlint.purify


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


left_double_quote = "“"
right_double_quote = "”"

left_single_quote = "‘"
right_single_quote = "’"

thin_sapce_break = " "
thin_space_nonbreak = " "

emdash = "—"
endash = "–"


def _quote_order_rule(name, single, double):
    rules = []
    rules.append((
        "quotation.missing-space-{}-single-double".format(name),
        _pair_regex(single, double)))
    rules.append((
        "quotation.missing-space-{}-double-single".format(name),
        _pair_regex(double, single)))

    return rules


def _double_punctuation_rule(name, quote):
    return [(
        "quotation.consecutive-{}-quotes".format(name),
        _pair_regex(quote, quote))]


def _correct_space_rule(name, single, double):
    def correct_space_builder(first, second):
        predicate = _regex_rule("{}\\s{}".format(first, second))

        def execute(text, fn):
            hit = False

            def check_pos(pos):
                nonlocal hit
                if text[
                        pos +
                        1] != thin_space_nonbreak:
                    fn(pos)
                    hit = True

            predicate(text, check_pos)
            return hit

        return execute

    return [("quotation.incorrect-space-{}-single-double".format(name),
             correct_space_builder(single, double)),
            ("quotation.incorrect-space-{}-double-single".format(name),
             correct_space_builder(double, single))]


def _get_quote_rules():
    rules = _quote_order_rule("opening",
                              left_single_quote,
                              left_double_quote)
    rules += _quote_order_rule("closing",
                               right_single_quote,
                               right_double_quote)

    rules += _double_punctuation_rule("opening",
                                      left_single_quote)
    rules += _double_punctuation_rule("closing",
                                      right_double_quote)

    rules += _correct_space_rule("opening",
                                 left_single_quote,
                                 left_double_quote)
    rules += _correct_space_rule("closing",
                                 right_single_quote,
                                 right_double_quote)

    return rules


def _get_dash_rules():
    rules = [("emdash.replace-double-hyphen",
              _regex_rule("\\-\\-")),
             ("emdash.preceeding-space",
              _pair_regex("\\s", emdash)),
             ("emdash.trailing-space",
              _pair_regex(emdash, "\\s"))]
    return rules


def _colon_rule(name, colon):
    rules = []
    # a colon might be followed by a digit if it's time
    if name == "colon":
        rules.append(("{}.missing-space".format(name),
                      _pair_regex(colon, "[^\\s\\d]")))
    elif name == "semicolon":
        rules.append(("{}.missing-space".format(name),
                      _pair_regex(colon, "\\S")))

    rules.append(("{}.preceeding-space".format(name),
                  _pair_regex("\\s", colon)))

    return rules


def _get_colon_rules():
    rules = []
    rules += _colon_rule("colon", ":")
    rules += _colon_rule("semicolon", ";")

    return rules


def _uppercase_ampm_builder(time_regex_with_space):
    rules = []

    def builder(first, second):
        ampm_regex_uppercase = "(?:[{}]\\.?{}\\.?)".format(first,
                                                           second)
        rules.append(("time.uppercase-{}{}".format(first, second),
                      _pair_regex(time_regex_with_space,
                                  ampm_regex_uppercase)))

    builder("AP", "m")
    builder("AP", "M")
    builder("ap", "M")

    return rules


def _get_time_rules():
    time_regex = "(?:1[0-2]|0?[1-9]):(?:[0-5][0-9])"
    time_regex_with_space = "(?:1[0-2]|0?[1-9]):(?:[0-5][0-9] ?)"
    ampm_regex = "(?:[AaPp]\\.?[Mm]\\.?)"
    ampm_regex_no_periods = "(?:[AaPp][Mm])"

    rules = []
    rules.append(("time.missing-periods",
                  _pair_regex(time_regex_with_space,
                              ampm_regex_no_periods)))
    rules.append(("time.missing-space",
                  _pair_regex(time_regex, ampm_regex)))
    rules += _uppercase_ampm_builder(time_regex_with_space)

    return rules


def _get_range_rules(pattern):
    rules = []
    rules.append(("endash.preceeding-space",
                  _regex_rule("{}\\s+{}\\s*{}".format(
                              pattern, endash,
                              pattern))))
    rules.append(("endash.trailing-space",
                  _regex_rule("{}\\s*{}\\s+{}".format(
                              pattern, endash,
                              pattern))))

    rules.append(("endash.replace-hyphen",
                  _regex_rule("{}\\s*-\\s*{}".format(
                              pattern, pattern))))
    rules.append(("endash.replace-emdash",
                  _regex_rule("{}\\s*{}\\s*{}".format(
                              pattern, emdash,
                              pattern))))

    return rules


def get_all_rules():
    rules = _get_quote_rules()
    rules += _get_dash_rules()
    rules += _get_colon_rules()
    rules += _get_time_rules()
    rules += _get_range_rules(R"\d+")

    return rules


def check_rules(rules, text, hit_fn):
    for (message, fn) in rules:
        fn(text, lambda pos: hit_fn(message, pos))


def check_handle(rules, handle, hit_fn, purifier=None):
    if not purifier:
        purifier = wlint.purify.text

    line_number = 0
    for text in handle:
        line_number += 1
        check_rules(
            rules,
            purifier(text),
            lambda message,
            pos: hit_fn(
                line_number,
                message,
                pos))
