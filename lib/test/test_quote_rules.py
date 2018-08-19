#!/usr/bin/python3

import unittest

import wlint.punctuation


def _run_rules(ut, text, expected_rule=None, expected_position=None):
    hit = False

    def hit_fn(rule_message, pos):
        nonlocal hit

        ut.assertEqual(rule_message, expected_rule)
        ut.assertEqual(pos, expected_position)
        hit = True

    wlint.punctuation.check_rules(ut.rules, text, hit_fn)
    if expected_position or expected_rule:
        ut.assertTrue(hit)


class TestQuotationRules(unittest.TestCase):
    def setUp(self):
        self.rules = wlint.punctuation._get_quote_rules()

    def test_double_quotes(self):
        text = "{}{}Don't use duplicate quotes.{}".format(wlint.punctuation.left_single_quote,
                                                          wlint.punctuation.left_single_quote,
                                                          wlint.punctuation.right_double_quote)
        _run_rules(self, text, "quotation.consecutive-opening-quotes", 0)

    def test_missing_space(self):
        text = "{}{}This is a nested quote{}{}{}".format(wlint.punctuation.left_double_quote,
                                                         wlint.punctuation.left_single_quote,
                                                         wlint.punctuation.right_single_quote,
                                                         wlint.punctuation.thin_space_nonbreak,
                                                         wlint.punctuation.right_double_quote)
        _run_rules(
            self,
            text,
            "quotation.missing-space-opening-double-single",
            0)

    def test_incorrect_space_plain(self):
        text = "{} {}This is a nested quote{}{}{}".format(wlint.punctuation.left_double_quote,
                                                          wlint.punctuation.left_single_quote,
                                                          wlint.punctuation.right_single_quote,
                                                          wlint.punctuation.thin_space_nonbreak,
                                                          wlint.punctuation.right_double_quote)
        _run_rules(
            self,
            text,
            "quotation.incorrect-space-opening-double-single",
            0)

    def test_incorrect_space_break(self):
        text = "{}{}{}This is a nested quote{}{}{}".format(wlint.punctuation.left_double_quote,
                                                           wlint.punctuation.thin_sapce_break,
                                                           wlint.punctuation.left_single_quote,
                                                           wlint.punctuation.right_single_quote,
                                                           wlint.punctuation.thin_space_nonbreak,
                                                           wlint.punctuation.right_double_quote)
        _run_rules(
            self,
            text,
            "quotation.incorrect-space-opening-double-single",
            0)


if __name__ == '__main__':
    unittest.main()
