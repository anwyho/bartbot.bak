import os
import unittest

from .context import useLocalhost
# from bartbot.utils.emoji import emoji, emoji_test



class test_emoji(unittest.TestCase):
    def setUp(self):
        self.var = 'hello'

    def test_passing(self):
        print(useLocalhost)
        self.assertTrue(True)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()