import unittest
from shared.utils.string_utils import slugify
from shared.localization.locale_manager import LocaleManager

class TestShared(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("Hello World"), "hello_world")

    def test_locale_manager(self):
        lm = LocaleManager("es-es")
        self.assertEqual(lm.locale, "es-es")

if __name__ == "__main__":
    unittest.main()
