from typing import Dict, Iterable, List, Set, Union
from . import rhymeUtils as ru
from .util import flatten
from .IOUtil import load_word_phone_dict
from .rhymeUtils import PermutedPhone, Permutation, Phone, permuted_phone_mapper
from .RhymeTrieNode import RhymeTrieNode
from .songStats import sort_words
from itertools import groupby

_rt: Union[RhymeTrieNode, None] = None

PhymeResult = Dict[int, List[str]]

class Phyme(object):
    '''Phyme: a rhyming dictionary for songwriting'''

    def __init__(self):
        self.rhyme_trie = load_rhyme_trie()

    def search_permutations(self, phones) -> PhymeResult:
        '''Search the rhyme trie for sub words given a listen of phones'''
        phones = list(phones)
        nodes = self.rhyme_trie.search_permutations(phones[::-1])
        result_set: Set[str] = set()
        for node in nodes:
            result = node.get_sub_words()
            result_set.update(result)
        sorted_results = sorted(result_set,
                                key=ru.count_syllables)
        grouped_results = groupby(sorted_results, key=ru.count_syllables)
        return dict((k, list(v)) for k, v in grouped_results)

    def sorted_search(self, phones:Iterable[Union[Phone, PermutedPhone]], keyword:str) -> PhymeResult:
        results = self.search_permutations(phones)
        sorted_dict: PhymeResult = dict()
        for k, v in results.items():
            sorted_dict[k] = sort_words(keyword, v)
        return sorted_dict

    def get_perfect_rhymes(self, word:str, num_syllables: int=-1) -> PhymeResult:
        """Get perfect rhymes of a word, defaults to last stressed vowel

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int} -- Number of syllables to check
                subtractive rhymes for (default: {-1}) for last stressed and
                unstressed

        Returns:
            [Dict[int, List[str]] - dict of lists of rhymes keyed by number
                of syllables
        """

        phones = ru.get_last_syllables(word, num_syllables)
        return self.sorted_search(list(flatten(phones)), word)

    def get_family_rhymes(self, word:str, num_syllables: int=-1) -> PhymeResult:
        '''
        Get words with the same vowel and stress patterns but with consonants
        from the same family (consonants with the same articulation and
        un/voiced) (DOG -> COB)

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int} -- Number of syllables to check
                subtractive rhymes for (default: {-1}) for last stressed and
                unstressed

        Returns:
            [Dict[int, List[str]] - dict of lists of rhymes keyed by number
                of syllables
        '''
        phones = ru.get_last_syllables(word, num_syllables)
        if not ru.is_consonant(phones[0][-1]):
            return dict()
        flattened_phones = flatten(phones)
        permuted_phones = map(permuted_phone_mapper(Permutation.FAMILY, ru.is_consonant), flattened_phones)
        return self.sorted_search(permuted_phones, word)

    def get_partner_rhymes(self, word:str, num_syllables: int=-1) -> PhymeResult:
        '''
        Get words with the same vowel and stress patterns but with partner
        consonants (consonants with the same articulation) (HAWK -> DOG)

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int} -- Number of syllables to check
                subtractive rhymes for (default: {-1}) for last stressed and
                unstressed

        Returns:
            [Dict[int, List[str]] - dict of lists of rhymes keyed by number
                of syllables
        '''
        phones = ru.get_last_syllables(word, num_syllables)
        if not ru.is_consonant(phones[0][-1]):
            return dict()
        flattened_phones = flatten(phones)

        permuted_phones = map(permuted_phone_mapper(Permutation.PARTNER, ru.is_consonant), flattened_phones)

        return self.sorted_search(permuted_phones, word)

    def get_additive_rhymes(self, word: str, num_syllables: int=-1) -> PhymeResult:
        '''
        Get words with the same vowel and stress patterns but including
        additional consonants (MATTER -> MASTER)

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int} -- Number of syllables to check
                subtractive rhymes for (default: {-1}) for last stressed and
                unstressed

        Returns:
            [Dict[int, List[str]] - dict of lists of rhymes keyed by number
                of syllables
        '''
        phones = ru.get_last_syllables(word, num_syllables)
        flattened_phones = list(flatten(phones))
        permuted_phones = list(map(permuted_phone_mapper(Permutation.ADDITIVE, lambda _: True), flattened_phones))

        return self.sorted_search(permuted_phones, word)

    def get_by_vowel(self, vowel: Phone) -> PhymeResult:
        if not vowel[-1].isnumeric():
            vowel = vowel + "1"
        phones = [PermutedPhone(vowel, Permutation.ADDITIVE)]
        return self.sorted_search(phones, vowel)

    def get_subtractive_rhymes(self, word, num_syllables=None) -> PhymeResult:
        '''
        Get words with the same vowel and stress patterns but dropping some
        consonants (MASTER -> MATTER)

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int} -- Number of syllables to check
                subtractive rhymes for (default: {-1}) for last stressed and
                unstressed

        Returns:
            [Dict[int, List[str]] - dict of lists of rhymes keyed by number
                of syllables
        '''
        phones = ru.get_last_syllables(word, num_syllables)
        if not ru.is_consonant(phones[0][-1]):
            return dict()
        flattened_phones = flatten(phones)
        permuted_phones = map(permuted_phone_mapper(Permutation.SUBTRACTIVE, ru.is_consonant), flattened_phones)

        return self.sorted_search(permuted_phones, word)

    def get_consonant_rhymes(self, word, num_syllables=None) -> PhymeResult:
        '''
        Get words with the same stress patterns and consonants but with
        arbitrary vowels (DOG -> BAG)

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int} -- Number of syllables to check
                subtractive rhymes for (default: {-1}) for last stressed and
                unstressed

        Returns:
            [Dict[int, List[str]] - dict of lists of rhymes keyed by number
                of syllables
        '''
        phones = ru.get_last_syllables(word, num_syllables)
        flattened_phones = flatten(phones)
        permuted_phones = map(permuted_phone_mapper(Permutation.CONSONANT, ru.is_vowel), flattened_phones)

        return self.sorted_search(permuted_phones, word)

    def get_assonance_rhymes(self, word, num_syllables=None) -> PhymeResult:
        '''
        Get words with the same vowels and stress patterns but arbitrary
        consonants (JAUNT -> DOG)

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int} -- Number of syllables to check
                subtractive rhymes for (default: {-1}) for last stressed and
                unstressed

        Returns:
            [Dict[int, List[str]] - dict of lists of rhymes keyed by number
                of syllables
        '''
        phones = ru.get_last_syllables(word, num_syllables)
        flattened_phones = list(flatten(phones))
        filtered_phones = list(filter(lambda phone: ru.is_vowel(phone), flattened_phones))
        permuted_phones = list(map(permuted_phone_mapper(Permutation.ASSONANCE, lambda _: True), filtered_phones))

        return self.sorted_search(permuted_phones, word)

    def get_substitution_rhymes(self, word, num_syllables=None) -> PhymeResult:
        '''
        Get words with the same vowels and stress patterns but substitute
        arbitrary consonants (FASTER -> FACTOR)

        Arguments:
            word {str} -- word to rhyme

        Keyword Arguments:
            num_syllables {int} -- Number of syllables to check
                subtractive rhymes for (default: {-1}) for last stressed and
                unstressed

        Returns:
            [Dict[int, List[str]] - dict of lists of rhymes keyed by number
                of syllables
        '''
        phones = ru.get_last_syllables(word, num_syllables)
        flattened_phones = flatten(phones)
        permuted_phones = map(permuted_phone_mapper(Permutation.SUBSTITUTION, ru.is_consonant), flattened_phones)
        return self.sorted_search(permuted_phones, word)


def load_rhyme_trie() -> RhymeTrieNode:
    global _rt
    if _rt:
        return _rt
    word_phone_dict = load_word_phone_dict()
    _rt = RhymeTrieNode(None, None)
    for word, phones in word_phone_dict.items():
        _rt.insert(phones[::-1], word)
    return _rt
