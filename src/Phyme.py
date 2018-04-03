import util
import rhymeUtils as ru
from IOUtil import load_word_phone_dict, load_phone_type_dicts, load_rhyme_trie


class Phyme(object):
    '''Phyme: a rhyming dictionary for songwriting'''

    def __init__(self):
        self.rhyme_trie = load_rhyme_trie()

    def search(self, phones):
        '''Search the rhyme trie for sub words given a listen of phones
        Returns a set of strings'''
        result = self.rhyme_trie.search(phones)
        if result:
            return set(result.get_sub_words())
        else:
            return None

    def get_perfect_rhymes(self, word, num_syllables=None):
        '''Get perfect rhymes of a word, based on its last stressed vowel'''
        phones = ru.get_last_syllables(word, num_syllables)
        results = self.search(list(util.flatten(phones)))
        if results:
            results.remove(word.upper())
            return results
        else:
            return set()

    def get_family_rhymes(self, word, num_syllables=None):
        phones = ru.get_last_syllables(word, num_syllables)
        # todo: this rhymes on first stressed syllable. possibly implement
        # multiple stressed syllable rhymes
        if not ru.is_consonant(phones[0][-1]):
            return set()
        results = set()
        for permutation in self._recursive_permute_words(phones, family=True):
            permutation = list(util.flatten(permutation))
            result = self.search(permutation)
            if result:
                results.update(result)
        return results

    def get_partner_rhymes(self, word, num_syllables=None):
        phones = ru.get_last_syllables(word, num_syllables)
        if not ru.is_consonant(phones[0][-1]):
            return set()
        results = set()
        for permutation in self._recursive_permute_words(phones, family=False):
            permutation = list(util.flatten(permutation))
            result = self.search(permutation)
            if result:
                results.update(result)
        return results

    def _recursive_permute_words(self, sylls, family=True):
        if len(sylls) == 1:
            yield from ([syll] for syll in
                        self._recursive_permute_syllable(sylls[0], family))
        else:
            for syll in self._recursive_permute_syllable(sylls[0], family):
                yield from ([syll] + rest for rest in
                            self._recursive_permute_words(sylls[1:], family))

    def _recursive_permute_syllable(self, phones, family=True):
        if len(phones) == 1:
            yield from ([companion] for companion in
                        self._permute_consonant(phones[0], family))
        else:
            if ru.is_vowel(phones[0]):
                yield from ([phones[0]] + list(rest) for rest in
                            self._recursive_permute_syllable(phones[1:],
                                                             family))
            else:
                for companion in self._permute_consonant(phones[0], family):
                    yield from ([companion] + list(rest) for rest in
                                self._recursive_permute_syllable(phones[1:],
                                                                 family))

    def _permute_consonant(self, consonant, family=True):
        if family:
            companions = ru.get_consonant_family(consonant)
        else:
            companions = ru.get_consonant_partners(consonant)
        yield from companions
