import rhymeUtils as ru
from IOUtil import load_word_phone_dict, load_phone_type_dicts, load_rhyme_trie


class Phyme(object):
    '''Phyme: a rhyming dictionary for songwriting'''

    def __init__(self):
        self.dict = load_word_phone_dict()
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

    def get_additive_rhymes(self, word):
        '''Get additve rhymes (PASS -> FAST)'''
        # TODO: find legitimate amalgamations of consonants?
        pass

    def get_subtractive_rhymes(self, word):
        '''Get subtractive rhymes (FAST -> PASS)'''
        pass

    def get_family_rhymes(self, word):
        '''Get rhymes from the same consonant family (type, voiced) (DOG -> COB)
        Design decisions:
        - should family rhyme be on stressed or unstressed syllables (or both?) 
        - how to handle composite 
        '''
        phones = ru.get_phones(word)
#         if is_consonant(phones[-1]):
#             for consonant in 
        
#         pass
    
    def get_partner_rhymes(self, word):
        '''Get rhymes from the same consonant groups (eg, fricative)'''
        pass
    
    def get_assonance_rhymes(self, word):
        '''Get rhymes that stress the same vowel'''
        pass
    
    def get_perfect_vowel_partner_rhymes(self, word):
        '''Get rhymes using similar vowels with the same consonant'''
        pass
    
    def get_family_vowel_partner_partner_rhymes(self, word):
        '''Get rhymes using similar values with consonant family'''
        pass
    
    def get_partner_vowel_partner_rhymes(self, word):
        '''Get rhymes with similar vowels with same consonant group'''
        pass
    
    def get_consonant_rhymes(self, word):
        '''Get rhymes that end with the same consonant'''
        pass
        