import unittest
import sys
sys.path.append('../')
from Phyme.Phyme import load_rhyme_trie
from Phyme.rhymeUtils import _word_phone_dict


class RhymeTrieTest(unittest.TestCase):
    rt = load_rhyme_trie()

    def test_search(self):
        for word, phones in _word_phone_dict.items():
            retrieved = self.rt.search(phones[::-1])
            self.assertTrue(word.lower() in retrieved.words)

    def test_get_sub_words(self):
        leven = self.rt.search(_word_phone_dict['LEVEN'][::-1])
        self.assertTrue('kleven' in set(leven.get_sub_words()))

    def test_contains(self):
        self.assertTrue(self.rt.contains(_word_phone_dict['DOG'][::-1]))


if __name__ == '__main__':
    unittest.main()
