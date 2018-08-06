#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

import word_ladder


class TestDict(unittest.TestCase):
    def test_checkUserInput(self):
        word_ladder.fname = 'dictionary.txt'
        word_ladder.start = 'lead'
        word_ladder.target = 'gold'
        word_ladder.steps = 3
        self.assertTrue(word_ladder.checkUserInput())

    def test_checkUserInput_Different_length(self):
        word_ladder.fname = 'dictionary.txt'
        word_ladder.start = 'hello'
        word_ladder.target = 'gold'
        word_ladder.steps = 3
        self.assertFalse(word_ladder.checkUserInput())

    def test_checkUserInput_not_found_file(self):
        word_ladder.fname = 'xxx.txt'
        word_ladder.start = 'lead'
        word_ladder.target = 'gold'
        word_ladder.steps = 3
        self.assertFalse(word_ladder.checkUserInput())

    def test_checkUserInput_number_in_word(self):
        word_ladder.fname = 'dictionary.txt'
        word_ladder.start = 'are1'
        word_ladder.target = 'gold'
        word_ladder.steps = 3
        self.assertFalse(word_ladder.checkUserInput())

    def test_checkUserInput_start_not_in_file(self):
        word_ladder.fname = 'dictionary.txt'
        word_ladder.start = 'llll'
        word_ladder.target = 'gold'
        word_ladder.steps = 3
        self.assertFalse(word_ladder.checkUserInput())

    def test_checkUserInput_target_not_in_file(self):
        word_ladder.fname = 'dictionary.txt'
        word_ladder.start = 'llll'
        word_ladder.target = 'gold'
        word_ladder.steps = 3
        self.assertFalse(word_ladder.checkUserInput())

    def test_checkUserInput_others_error(self):
        word_ladder.fname = ''
        word_ladder.start = ''
        word_ladder.target = ''
        word_ladder.steps = ''
        self.assertFalse(word_ladder.checkUserInput())

    def test_checkWord_True(self):
        self.assertFalse(word_ladder.checkWord('word'))

    def test_checkWord_False(self):
        self.assertTrue(word_ladder.checkWord('wo0d'))

    def test_isInDictionary_True(self):
        word_ladder.checkUserInput()
        self.assertFalse(word_ladder.isInDictionary('word'))

    def test_isInDictionary_False(self):
        word_ladder.checkUserInput()
        self.assertTrue(word_ladder.isInDictionary('wordttt'))

    def test_build0(self):
        word_ladder.checkUserInput()
        word_ladder.findWords()
        self.assertEqual(word_ladder.build0('lead', word_ladder.words, word_ladder.seen),
                         ['bead', 'dead', 'head', 'leaf', 'leak', 'leal', 'lean', 'leap', 'lear', 'leas', 'lend',
                          'leud', 'lewd', 'load', 'mead', 'read'])

    def test_findWorld_len(self):
        word_ladder.checkUserInput()
        word_ladder.findWords()
        self.assertEqual(word_ladder.words.__len__(), 3862)

    def test_isDifferOne_True(self):
        self.assertTrue(word_ladder.isDifferOne('abc', 'abd'))

    def test_isDifferOne_False(self):
        self.assertFalse(word_ladder.isDifferOne('abc', 'aee'))

    def test_getShortist(self):
        self.assertEqual(word_ladder.getShortist([[1, 2, 3], [1, 2], [1, 2, 3, 4, 5]]), [1, [[1, 2]]])

    def test_find(self):
        word_ladder.checkUserInput()
        word_ladder.findWords()
        word_ladder.find(word_ladder.start, word_ladder.words, word_ladder.seen, word_ladder.target, word_ladder.path)
        self.assertEqual(word_ladder.paths, [['lead', 'load', 'goad', 'gold']])


if __name__ == '__main__':
    unittest.main()
