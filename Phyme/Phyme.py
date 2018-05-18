from . import rhymeUtils as ru
from .util import flatten
from .IOUtil import load_word_phone_dict, load_phone_type_dicts
from .rhymeUtils import PermutedPhone, Permutations
from .RhymeTrieNode import RhymeTrieNode
from .songStats import sort_words
from itertools import groupby

_rt = None


class Phyme(object):
    '''Phyme: a rhyming dictionary for songwriting'''

    def __init__(self):
        self.rhyme_trie = load_rhyme_trie()

    def search_permutations(self, phones):
        '''Search the rhyme trie for sub words given a listen of phones'''
        phones = list(phones)
        nodes = self.rhyme_trie.search_permutations(phones[::-1])
        result_set = set()
        for node in nodes:
            result = node.get_sub_words()
            result_set.update(result)
        sorted_results = sorted(result_set,
                                key=ru.count_syllables)
        grouped_results = groupby(sorted_results, key=ru.count_syllables)
        return dict((k, list(v)) for k, v in grouped_results)

    def sorted_search(self, phones, keyword):
        results = self.search_permutations(phones)
        sorted_dict = dict()
        for k, v in results.items():
            sorted_dict[k] = sort_words(keyword, v)
        return sorted_dict

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
        return self.sorted_search(list(flatten(phones)), word)

    def get_family_rhymes(self, word, num_syllables=None):
        '''
        Get words with the same vowel and stress patterns but with consonants
        from the same family (consonants with the same articulation and
        un/voiced) (DOG -> COB)

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int | None} -- Number of syllables to check
                subtractive rhymes for (default: {None}) for last stressed and
                unstressed

        Returns:
            [set] -- set of rhymes
        '''
        phones = ru.get_last_syllables(word, num_syllables)
        if not ru.is_consonant(phones[0][-1]):
            return dict()
        phones = flatten(phones)
        phones = map(lambda phone: PermutedPhone(phone, Permutations.FAMILY)
                     if ru.is_consonant(phone)
                     else phone,
                     phones)
        return self.sorted_search(phones, word)

    def get_partner_rhymes(self, word, num_syllables=None):
        '''
        Get words with the same vowel and stress patterns but with partner
        consonants (consonants with the same articulation) (HAWK -> DOG)

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int | None} -- Number of syllables to check
                subtractive rhymes for (default: {None}) for last stressed and
                unstressed

        Returns:
            [set] -- set of rhymes
        '''
        phones = ru.get_last_syllables(word, num_syllables)
        if not ru.is_consonant(phones[0][-1]):
            return dict()
        phones = flatten(phones)
        phones = map(lambda phone: PermutedPhone(phone, Permutations.PARTNER)
                     if ru.is_consonant(phone)
                     else phone,
                     phones)
        return self.sorted_search(phones, word)

    def get_additive_rhymes(self, word, num_syllables=None):
        '''
        Get words with the same vowel and stress patterns but including
        additional consonants (MATTER -> MASTER)

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int | None} -- Number of syllables to check
                subtractive rhymes for (default: {None}) for last stressed and
                unstressed

        Returns:
            [set] -- set of rhymes
        '''
        phones = ru.get_last_syllables(word, num_syllables)
        phones = flatten(phones)
        phones = map(lambda phone: PermutedPhone(phone, Permutations.ADDITIVE),
                     phones)
        return self.sorted_search(phones, word)

    def get_subtractive_rhymes(self, word, num_syllables=None):
        '''
        Get words with the same vowel and stress patterns but dropping some
        consonants (MASTER -> MATTER)

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int | None} -- Number of syllables to check
                subtractive rhymes for (default: {None}) for last stressed and
                unstressed

        Returns:
            [set] -- set of rhymes
        '''
        phones = ru.get_last_syllables(word, num_syllables)
        if not ru.is_consonant(phones[0][-1]):
            return dict()
        phones = flatten(phones)
        phones = map(lambda phone: PermutedPhone(phone, Permutations.SUBTRACTIVE)
                     if ru.is_consonant(phone)
                     else phone,
                     phones)
        return self.sorted_search(phones, word)

    def get_consonant_rhymes(self, word, num_syllables=None):
        '''
        Get words with the same stress patterns and consonants but with
        arbitrary vowels (DOG -> BAG)

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int | None} -- Number of syllables to check
                subtractive rhymes for (default: {None}) for last stressed and
                unstressed

        Returns:
            [set] -- set of rhymes
        '''
        phones = ru.get_last_syllables(word, num_syllables)
        phones = flatten(phones)
        phones = map(lambda phone: PermutedPhone(phone, Permutations.CONSONANT)
                     if ru.is_vowel(phone)
                     else phone,
                     phones)
        return self.sorted_search(phones, word)

    def get_assonance_rhymes(self, word, num_syllables=None):
        '''
        Get words with the same vowels and stress patterns but arbitrary
        consonants (JAUNT -> DOG)

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int | None} -- Number of syllables to check
                subtractive rhymes for (default: {None}) for last stressed and
                unstressed

        Returns:
            [set] -- set of rhymes
        '''
        phones = ru.get_last_syllables(word, num_syllables)
        phones = flatten(phones)
        phones = map(lambda phone: PermutedPhone(phone, Permutations.ADDITIVE),
                     filter(lambda phone: ru.is_vowel(phone), phones))
        return self.sorted_search(phones, word)

    def get_substitution_rhymes(self, word, num_syllables=None):
        '''
        Get words with the same vowels and stress patterns but substitute
        arbitrary consonants (FASTER -> FACTOR)

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int | None} -- Number of syllables to check
                subtractive rhymes for (default: {None}) for last stressed and
                unstressed

        Returns:
            [set] -- set of rhymes
        '''
        phones = ru.get_last_syllables(word, num_syllables)
        phones = flatten(phones)
        phones = map(lambda phone: PermutedPhone(phone, Permutations.SUBSTITUTION)
                     if ru.is_consonant(phone)
                     else phone,
                     phones)
        return self.sorted_search(phones, word)


def load_rhyme_trie():
    global _rt
    if _rt:
        return _rt
    word_phone_dict = load_word_phone_dict()
    _rt = RhymeTrieNode(None, None)
    for word, phones in word_phone_dict.items():
        _rt.insert(phones[::-1], word)
    return _rt
