import unittest
import sys
sys.path.append('../')
from Phyme.Phyme import load_rhyme_trie
from Phyme.rhymeUtils import Phone, _word_phone_dict


class RhymeTrieTest(unittest.TestCase):
    rt = load_rhyme_trie()

    def test_search(self):
        for word, string_phones in _word_phone_dict.items():
            phones = [Phone(phone) for phone in string_phones]
            retrieved = self.rt.search(phones[::-1])
            self.assertIsNotNone(retrieved)
            assert retrieved is not None
            self.assertIsNotNone(retrieved)
            self.assertTrue(word.lower() in retrieved.words)

    def test_get_sub_words(self):
        string_phones = _word_phone_dict['LEVEN']
        phones = [Phone(phone) for phone in string_phones]
        leven = self.rt.search(phones[::-1])
        self.assertIsNotNone(leven)
        assert leven is not None
        self.assertTrue('kleven' in set(leven.get_sub_words()))

    def test_contains(self):
        string_phones = _word_phone_dict['DOG']
        phones = [Phone(phone) for phone in string_phones]
        self.assertTrue(self.rt.contains(phones[::-1]))


if __name__ == '__main__':
    unittest.main()
