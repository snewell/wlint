#!/usr/bin/python3

import wlint.punctuation

_LEFT_DOUBLE_QUOTE = "“"
_RIGHT_DOUBLE_QUOTE = "”"

_LEFT_SINGLE_QUOTE = "‘"
_RIGHT_SINGLE_QUOTE = "’"

_THIN_SAPCE_BREAK = " "
_THIN_SPACE_NONBREAK = " "


def _make_quote_order_rule(name, single, double):
    rules = []
    rules.append((
        "quotation.missing-space-{}-single-double".format(name),
        wlint.punctuation.make_pair_regex_rule(single, double)))
    rules.append((
        "quotation.missing-space-{}-double-single".format(name),
        wlint.punctuation.make_pair_regex_rule(double, single)))

    return rules


def _double_punctuation_rule(name, quote):
    return [(
        "quotation.consecutive-{}-quotes".format(name),
        wlint.punctuation.make_pair_regex_rule(quote, quote))]


def _correct_space_rule(name, single, double):
    def correct_space_builder(first, second):
        predicate = wlint.punctuation.make_regex_rule(
            "{}\\s{}".format(first, second))

        def execute(text, fn):
            hit = False

            def check_pos(pos):
                nonlocal hit
                if text[
                        pos +
                        1] != _THIN_SPACE_NONBREAK:
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
    rules = _make_quote_order_rule("opening",
                                   _LEFT_SINGLE_QUOTE,
                                   _LEFT_DOUBLE_QUOTE)
    rules += _make_quote_order_rule("closing",
                                    _RIGHT_SINGLE_QUOTE,
                                    _RIGHT_DOUBLE_QUOTE)

    rules += _double_punctuation_rule("opening",
                                      _LEFT_SINGLE_QUOTE)
    rules += _double_punctuation_rule("closing",
                                      _RIGHT_DOUBLE_QUOTE)

    rules += _correct_space_rule("opening",
                                 _LEFT_SINGLE_QUOTE,
                                 _LEFT_DOUBLE_QUOTE)
    rules += _correct_space_rule("closing",
                                 _RIGHT_SINGLE_QUOTE,
                                 _RIGHT_DOUBLE_QUOTE)

    return rules


_QUOTE_RULES = _get_quote_rules()
