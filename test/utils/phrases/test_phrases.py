import time
import unittest

from types import ModuleType

# TODO: Should I add support here for en_UD and en_GB?

from bartbot.utils.phrases import (emojis, locales, phrase)

from ...context import use_localhost

class TestPhrase(unittest.TestCase):

    def test_set_locale_to_default_locale(self):
        localeModule = phrase.set_locale()
        self.assertIsInstance(localeModule, ModuleType, 
            "phrase.set_locale() should have a default locale")
        self.assertIsNotNone(localeModule.phrases, 
            "Locale module should have a phrases dict")
    
    def test_set_locale_to_supported_locale(self):
        localeModule = phrase.set_locale("en_gb")
        self.assertIsInstance(localeModule, ModuleType)
        self.assertIsNotNone(localeModule.phrases, 
            "Locale module should have a phrases dict")

    def test_set_locale_to_unsupported_locale(self):
        localeModule = phrase.set_locale("na_NA")
        self.assertIsInstance(localeModule, ModuleType, 
            "phrase.set_locale() should set locale to default locale if unsupported locale is given")
        self.assertIsNotNone(localeModule.phrases, 
            "Locale module should have a phrases dict")

    def test_get_phrase(self):
        _ = phrase.set_locale()
        self.assertNotEqual(phrase.get_phrase('hello'), "")

    def test_get_phrase_with_multiple_inputs(self):
        _ = phrase.set_locale()
        self.assertNotEqual(phrase.get_phrase('hello', 'bye'), "")
    
    def test_get_phrase_with_invalid_input(self):
        _ = phrase.set_locale()
        self.assertEqual(phrase.get_phrase('test invalid input'), 
            "test invalid input", "phrase.get_phrase() should print invalid keys")
    
    def test_get_phrase_with_multiple_invalid_inputs(self):
        _ = phrase.set_locale()
        self.assertEqual(phrase.get_phrase('mult!ple', 'inv@lid', '!nputs'), "mult!ple inv@lid !nputs", 
            "phrase.get_phrase() should join invalid string keys with spaces")

    def test_get_phrase_speed(self):
        import time as t
        localePhrases = phrase.set_locale()
        NUM_CALLS = 1000
        start = t.time()
        for _ in range(NUM_CALLS):
            phrase.get_phrase(*(localePhrases.phrases.keys()))
        elapsed = t.time()-start
        avg = elapsed/NUM_CALLS
        # Shouldn't hang for more than a millisecond on average
        self.assertTrue(avg*1000 < 1, 
            "Average phrase.get_phrase speed should be less than a millisecond")  



class TestEmoji(unittest.TestCase):
    def test_print_all_emojis(self):
        if len(emojis.emojis):
            self.assertNotEqual(emojis.print_all_emojis(), "", 
                "Emoji test is not working")



class TestPhrasesEnUs(unittest.TestCase):
    def test_phrases_composition(self):
        localePhrases = phrase.set_locale("en_us")
        for phraseType, phraseList in localePhrases.phrases.items():
            self.assertIsInstance(phraseType, str, 
                "Phrase dicts must have strings as keys")
            self.assertIsInstance(phraseList, list, 
                "Phrase dicts must have lists of strings as values")
            for item in phraseList:
                self.assertIsInstance(item, str, 
                    "Phrase dicts must have lists of strings as values")
                self.assertEqual(item.strip(), item, 
                    "Phrases should not contain leading or trailing spaces")



if __name__ == '__main__':
    unittest.main()