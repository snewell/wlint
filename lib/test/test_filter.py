#/usr/bin/python3

import unittest

import env

import wlint.filter
import wlint.purify


class TestWordList(unittest.TestCase):
    def test_ctor(self):
        wl = wlint.filter.WordList()
        self.assertEqual(len(wl.words), 0)

    def test_add_word(self):
        wl = wlint.filter.WordList()
        wl.addWord("hello")
        self.assertEqual(len(wl.words), 1)

    def test_add_duplicate_word(self):
        wl = wlint.filter.WordList()
        wl.addWord("hello")
        wl.addWord("hello")
        self.assertEqual(len(wl.words), 1)


class TestFilter(unittest.TestCase):
    def setUp(self):
        self.wl = wlint.filter.WordList()
        self.purifier = wlint.purify.text

    def test_ctor(self):
        filt = wlint.filter.Filter(self.wl, self.purifier)


if __name__ == '__main__':
    unittest.main()
