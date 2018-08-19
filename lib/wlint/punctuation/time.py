#!/usr/bin/python3

import wlint.punctuation


def _uppercase_ampm_builder(time_regex_with_space):
    rules = []

    def builder(first, second):
        ampm_regex_uppercase = "(?:[{}]\\.?{}\\.?)".format(first,
                                                           second)
        rules.append(("time.uppercase-{}{}".format(first, second),
                      wlint.punctuation.make_pair_regex_rule(time_regex_with_space,
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
                  wlint.punctuation.make_pair_regex_rule(time_regex_with_space,
                                                         ampm_regex_no_periods)))
    rules.append(("time.missing-space",
                  wlint.punctuation.make_pair_regex_rule(time_regex, ampm_regex)))
    rules += _uppercase_ampm_builder(time_regex_with_space)

    return rules


_TIME_RULES = _get_time_rules()
