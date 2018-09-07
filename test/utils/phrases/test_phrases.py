import unittest

# TODO: Should I add support here for en_UD and en_GB?

from bartbot.utils.phrases import phrase

from ...context import use_localhost

class TestPhrases_en_US(unittest.TestCase):
    def setUp(self):
        self.var = 'hello'

    def test_get_phrase_speed(self):
        self.assertTrue(True)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()