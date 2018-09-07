import unittest

from bartbot.utils.phrases import emoji as e

class test_emoji(unittest.TestCase):

    def test_print_all_emojis(self):
        if len(e.emojis):
            self.assertNotEqual(e.print_all_emojis(), "")


if __name__ == '__main__':
    unittest.main()