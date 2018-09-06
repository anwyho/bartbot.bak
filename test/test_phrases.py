import bartbot

import os
import unittest

class TestPhrases(unittest.TestCase):
    def setUp(self):
        self.var = 'hello'

    def test_passing(self):
        self.assertTrue(True)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()