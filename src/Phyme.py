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

    def get_perfect_rhymes(self, word, num_syllables=1):
        '''Get perfect rhymes of a word, based on its last stressed vowel'''
        phones = ru.get_last_syllable(word, num_syllables)
        results = self.search(phones)
        if results:
            results.remove(word.upper())
        return results
    
    def get_family_rhymes(self, word, num_syllables=1):
        phones = ru.get_last_syllable(word, num_syllables)
        if not ru.is_consonant(phones[-1]):
            return set()
        consonant = phones[-1]
        family = ru.get_consonant_family(consonant)
        family.remove(consonant)
        results = set()
        for consonant in family:
            results.update(self.search(phones[:-1] + [consonant]))
        return results
