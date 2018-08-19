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


class TestDashRules(unittest.TestCase):
    def setUp(self):
        self.rules = wlint.punctuation._get_dash_rules()

    def test_double_hyphen(self):
        text = "Asides--although odd{}are useful.".format(
            wlint.punctuation.emdash)
        _run_rules(self, text, "emdash.replace-double-hyphen", 6)

    def test_leading_space(self):
        text = "The woman opened her door {}she screamed.".format(
            wlint.punctuation.emdash)
        _run_rules(self, text, "emdash.preceeding-space", 25)

    def test_trailing_space(self):
        text = "The woman opened her door{} she screamed.".format(
            wlint.punctuation.emdash)
        _run_rules(self, text, "emdash.trailing-space", 25)


if __name__ == '__main__':
    unittest.main()
