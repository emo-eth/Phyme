import rhymeUtils as ru
from IOUtil import load_word_phone_dict, load_phone_type_dicts, load_rhyme_trie


class Phyme(object):
    '''Phyme: a rhyming dictionary for songwriting'''

    def __init__(self):
        self.rhyme_trie = load_rhyme_trie()

    def search(self, phones):
        '''Search the rhyme trie for sub words given a listen of phones
        Returns a set of strings'''
        return set(self.rhyme_trie.search(phones).get_sub_words())

    def get_perfect_rhymes(self, word):
        '''Get perfect rhymes of a word, based on its last stressed vowel'''
        phones = ru.get_phones(word)
        results = self.search(phones)
        if results:
            results.remove(word.upper())
        return results
