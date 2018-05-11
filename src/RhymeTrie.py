from RhymeTrieNode import RhymeTrieNode
from IOUtil import load_word_phone_dict
from rhymeUtils import PermutedPhone, Permutations, permutation_getters
import rhymeUtils as ru

rt = None


class RhymeTrie(object):
    '''A RhymeTrie holds RhymeTrie nodes and accesses them.'''

    def __init__(self):
        self.children = {}

    def insert(self, phones, word):
        '''Given a word and its phones, insert them into the trie. Associate the word with the end node.
        Returns a RhymeTrieNode'''
        # TODO: fix arms length?
        # reverse phones to search down trie
        phones = phones[::-1]
        child_node = self.children.get(phones[0])
        if child_node is None:
            child_node = RhymeTrieNode(phones[0], self)
            self.children[phones[0]] = child_node
        remaining_phones = phones[1:]
        if remaining_phones:
            final_node = child_node.insert(remaining_phones)
            final_node.words.add(word)
            return final_node
        else:
            child_node.words.add(word)
            return child_node

    def contains(self, phones):
        '''Given a list of phones, finds the end node in the trie associated with those phones.
        Returns a RhymeTrieNode'''
        phones = phones[::-1]
        child_node = self.children.get(phones[0])
        remaining_phones = phones[1:]
        if child_node:
            return child_node.contains(remaining_phones)
        return False

    def search(self, phones):
        '''Given a list of phones, find a node in the trie associated with those phones.
        Returns a RhymeTrieNode or None if there is no node associated with the given phones'''
        # reverse phones to search down trie
        phones = phones[::-1]
        child_node = self.children.get(phones[0])
        remaining_phones = phones[1:]
        if child_node:
            return child_node.search(remaining_phones)
        return None

    def search_permutations(self, phones):
        '''Returns a generator of nodes'''
        phones = phones[::-1]
        yield from self._add_subtract_phones(phones)
        permuted_phones = self._get_permuted_phones(phones[0])
        remaining_phones = phones[1:]
        for phone in permuted_phones:
            child = self.children.get(phone)
            if child:
                yield from child.search_permutations(remaining_phones)

    def count_nodes(self):
        '''Counts the number of children nodes in the trie'''
        return sum(child.count_nodes() for child in self.children.values())

    def count_words(self):
        '''Counts the number of words in the trie'''
        return sum(child.count_words() for child in self.children.values())

    def _get_permuted_phones(self, phone):
        if isinstance(phone, PermutedPhone):
            getter = permutation_getters.get(phone.permutation)
            yield from getter(phone.phone)
        else:
            yield phone

    def _add_subtract_phones(self, phones):
        if isinstance(phones[0], PermutedPhone):
            phone = phones[0]
            # try all permutations without this phone
            if phone.permutation == Permutations.SUBTRACTIVE:
                yield from self.search_permutations(phones[1:])
            elif phone.permutation == Permutations.ADDITIVE:
                for consonant in ru.CONSONANTS:
                    # try all permutations with this added consonant
                    child = self.children.get(consonant)
                    if child:
                        yield from child.search_permutations(phones)


def load_rhyme_trie():
    '''Load a fully-loaded RhymeTrie object'''
    global rt
    word_phone_dict = load_word_phone_dict()
    if rt:
        return rt
    rt = RhymeTrie()
    for word, phones in word_phone_dict.items():
        rt.insert(phones, word)
    return rt
