import util
import rhymeUtils as ru
from IOUtil import load_word_phone_dict, load_phone_type_dicts
from RhymeTrieNode import load_rhyme_trie
from rhymeUtils import PermutedPhone, Permutations


class Phyme(object):
    '''Phyme: a rhyming dictionary for songwriting'''

    def __init__(self):
        self.rhyme_trie = load_rhyme_trie()

    def search(self, phones):
        '''Search the rhyme trie for sub words given a listen of phones
        Returns a set of strings'''
        result = self.rhyme_trie.search(phones[::-1])
        if result:
            return set(result.get_sub_words())
        else:
            return None

    def search_permutations(self, phones):
        phones = list(phones)
        nodes = set(self.rhyme_trie.search_permutations(phones[::-1]))
        master_set = set()
        for node in nodes:
            result = node.get_sub_words()
            master_set.update(result)
        return master_set

    def get_perfect_rhymes(self, word, num_syllables=None):
        """Get perfect rhymes of a word, defaults to last stressed vowel

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int | None} -- Number of syllables to check
                subtractive rhymes for (default: {None}) for last stressed and
                unstressed

        Returns:
            [set] -- set of rhymes
        """

        phones = ru.get_last_syllables(word, num_syllables)
        results = self.search(list(util.flatten(phones)))
        if results:
            results.remove(word.upper())
            return results
        else:
            return set()

    def get_family_rhymes(self, word, num_syllables=None):
        phones = ru.get_last_syllables(word, num_syllables)
        if not ru.is_consonant(phones[0][-1]):
            return set()
        phones = util.flatten(phones)
        phones = map(lambda phone: PermutedPhone(phone, Permutations.FAMILY)
                     if ru.is_consonant(phone)
                     else phone,
                     phones)
        return self.search_permutations(phones)

    def get_partner_rhymes(self, word, num_syllables=None):
        phones = ru.get_last_syllables(word, num_syllables)
        if not ru.is_consonant(phones[0][-1]):
            return set()
        phones = util.flatten(phones)
        phones = map(lambda phone: PermutedPhone(phone, Permutations.PARTNER)
                     if ru.is_consonant(phone)
                     else phone,
                     phones)
        return self.search_permutations(phones)

    def get_additive_rhymes(self, word, num_syllables=None):
        phones = ru.get_last_syllables(word, num_syllables)
        phones = util.flatten(phones)
        phones = map(lambda phone: PermutedPhone(phone, Permutations.ADDITIVE),
                     phones)
        return self.search_permutations(phones)

    def get_subtractive_rhymes(self, word, num_syllables=None):
        phones = ru.get_last_syllables(word, num_syllables)
        if not ru.is_consonant(phones[0][-1]):
            return set()
        results = set()
        phones = util.flatten(phones)
        phones = map(lambda phone: PermutedPhone(phone, Permutations.SUBTRACTIVE)
                     if ru.is_consonant(phone)
                     else phone,
                     phones)
        return self.search_permutations(phones)

    def get_consonant_rhymes(self, word, num_syllables=None):
        phones = ru.get_last_syllables(word, num_syllables)
        phones = util.flatten(phones)
        phones = map(lambda phone: PermutedPhone(phone, Permutations.CONSONANT)
                     if ru.is_vowel(phone)
                     else phone,
                     phones)
        return self.search_permutations(phones)

    def get_assonance_rhymes(self, word, num_syllables=None):
        phones = ru.get_last_syllables(word, num_syllables)
        phones = util.flatten(phones)
        phones = map(lambda x: PermutedPhone(x, Permutations.ADDITIVE),
                     filter(lambda x: ru.is_vowel(x), phones))
        return self.search_permutations(phones)
