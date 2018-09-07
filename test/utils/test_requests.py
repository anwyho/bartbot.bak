import os
import unittest

from bartbot.utils import requests as breq

from ..context import (test_url, use_localhost)


class test_requests(unittest.TestCase):
    def setUp(self):
        self.var = 'hello'

    def test_get_phrase_speed(self):
        self.assertTrue(True)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()




