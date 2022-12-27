import unittest
from Phyme.Phyme import load_rhyme_trie
from Phyme.rhymeUtils import Phone, RhymeUtils


class RhymeTrieTest(unittest.TestCase):
    rt = load_rhyme_trie()

    def test_search(self):
        for word, string_phones in RhymeUtils._word_phone_dict.items():
            phones = [Phone(phone) for phone in string_phones]
            retrieved = self.rt.search(phones[::-1])
            self.assertIsNotNone(retrieved)
            assert retrieved is not None
            self.assertIsNotNone(retrieved)
            self.assertTrue(word.lower() in retrieved.words)

    def test_get_sub_words(self):
        string_phones = RhymeUtils._word_phone_dict.get("LEVEN")
        assert string_phones is not None
        phones = [Phone(phone) for phone in string_phones]
        leven = self.rt.search(phones[::-1])
        self.assertIsNotNone(leven)
        assert leven is not None
        self.assertTrue("kleven" in set(leven.get_sub_words()))

    def test_contains(self):
        string_phones = RhymeUtils._word_phone_dict.get("DOG")
        assert string_phones is not None
        phones = [Phone(phone) for phone in string_phones]
        self.assertTrue(self.rt.contains(phones[::-1]))


if __name__ == "__main__":
    unittest.main()
