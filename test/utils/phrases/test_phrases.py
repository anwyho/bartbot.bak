import time
import unittest

from types import ModuleType

# TODO: Should I add support here for en_UD and en_GB?

from bartbot.utils.phrases import phrase

from ...context import use_localhost

class TestPhrase(unittest.TestCase):

    def test_set_locale_to_default_locale(self):
        localeModule = phrase.set_locale()
        self.assertIsInstance(localeModule, ModuleType)
        self.assertIsNotNone(localeModule.phrases)
    
    def test_set_locale_to_supported_locale(self):
        localeModule = phrase.set_locale("en_gb")
        self.assertIsInstance(localeModule, ModuleType)
        self.assertIsNotNone(localeModule.phrases)

    def test_set_locale_to_unsupported_locale(self):
        localeModule = phrase.set_locale("na_NA")
        self.assertIsInstance(localeModule, None)
        self.assertIsNotNone(localeModule.phrases)

    def test_get_phrase(self):
        localeModule = phrase.set_locale()
        self.assertNotEqual(localeModule.phrase.get_phrase(), "")

    def test_get_phrase_with_multiple_inputs(self):
        pass
    
    def test_get_phrase_with_invalid_input(self):
        pass
    
    def test_get_phrase_with_multiple_invalid_inputs(self):
        pass

    def test_get_phrase_speed(self):
        
        self.assertTrue(True)

    def tearDown(self):
        pass


class TestPhrasesEnUs(unittest.TestCase):
    def test_get_phrase(self):
        pass


if __name__ == '__main__':
    unittest.main()