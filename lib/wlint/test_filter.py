#/usr/bin/python3

import unittest

import filter
import purify


class TestWordList(unittest.TestCase):
    def test_ctor(self):
        wl = filter.WordList()
        self.assertEqual(len(wl.words), 0)

    def test_add_word(self):
        wl = filter.WordList()
        wl.addWord("hello")
        self.assertEqual(len(wl.words), 1)

    def test_add_duplicate_word(self):
        wl = filter.WordList()
        wl.addWord("hello")
        wl.addWord("hello")
        self.assertEqual(len(wl.words), 1)


class TestFilter(unittest.TestCase):
    def setUp(self):
        self.wl = filter.WordList()
        self.purifier = purify.text

    def test_ctor(self):
        filt = filter.Filter(self.wl, self.purifier)

if __name__ == '__main__':
    unittest.main()
