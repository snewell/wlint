#/usr/bin/python3

import unittest

import env

import wlint.filter
import wlint.purify


class TestWordList(unittest.TestCase):
    def setUp(self):
        self.wl = wlint.filter.WordList()

    def test_ctor(self):
        self.assertEqual(len(self.wl.words), 0)

    def test_add_word(self):
        self.wl.add_word("hello")
        self.assertEqual(len(self.wl.words), 1)
        self.assertTrue("hello" in self.wl.words)

    def test_add_duplicate_word(self):
        self.wl.add_word("hello")
        self.wl.add_word("hello")
        self.assertEqual(len(self.wl.words), 1)
        self.assertTrue("hello" in self.wl.words)

    def test_add_sequence(self):
        self.wl.add_word_sequence(["hello", "world"])
        self.assertEqual(len(self.wl.words), 2)
        self.assertTrue("hello" in self.wl.words)
        self.assertTrue("world" in self.wl.words)


class TestFilter(unittest.TestCase):
    def _run_filter(self, sequence, expected):
        hits = {}

        def build_hits(word, line, column):
            nonlocal hits
            hits[(line, column)] = word

        self.filt.filter_sequence(sequence, build_hits)
        self.assertEqual(len(hits), len(expected))
        for (key, value) in expected.items():
            self.assertTrue(key in expected)
            self.assertEqual(hits[key], expected[key])

    def setUp(self):
        self.wl = wlint.filter.WordList()
        self.filt = wlint.filter.Filter(self.wl)

    def test_single(self):
        self.wl.add_word("hello")
        text = [
            "hello world"
        ]
        expected = {
            (1, 0): "hello"
        }
        self._run_filter(text, expected)

    def test_multiple(self):
        self.wl.add_word("hello")
        self.wl.add_word("world")
        text = [
            "hello world"
        ]
        expected = {
            (1, 0): "hello",
            (1, 6): "world"
        }
        self._run_filter(text, expected)


if __name__ == '__main__':
    unittest.main()
