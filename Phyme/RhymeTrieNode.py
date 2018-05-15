from .rhymeUtils import (PermutedPhone, Permutations, permutation_getters,
                         CONSONANTS)


class RhymeTrieNode(object):

    def __init__(self, phone, parent):
        self.children = {}
        self.parent = parent
        self.phone = phone
        self.words = set()

    def insert(self, phones, word):
        '''Insert a list of phones into this node and its children. Returns the final node of the insert.'''
        if not phones:
            self.words.add(word)
            return self
        child_node = self.children.get(phones[0])
        if child_node is None:
            child_node = RhymeTrieNode(phones[0], self)
            self.children[phones[0]] = child_node
        remaining_phones = phones[1:]
        return child_node.insert(remaining_phones, word)

    def contains(self, phones):
        '''Given a list of phones, finds the end node in the trie associated with those phones.
        Returns a RhymeTrieNode or False if there is no end node associated with the given phones'''
        if phones:
            child_node = self.children.get(phones[0])
            if child_node:
                return child_node.search(phones[1:])
        elif self.words:
            return self
        return False

    def search(self, phones):
        '''Given a list of phones, find a node in the trie associated with those phones.
        Returns a RhymeTrieNode or None if there is no node associated with the given phones'''
        if not phones:
            return self
        child_node = self.children.get(phones[0])
        if child_node:
            return child_node.search(phones[1:])
        return None

    def search_permutations(self, phones):
        '''Returns a generator of nodes'''
        if not phones:
            yield self
            return
        yield from self._add_subtract_phones(phones)
        permuted_phones = self._get_permuted_phones(phones[0])
        remaining_phones = phones[1:]
        for phone in permuted_phones:
            child = self.children.get(phone)
            if child:
                yield from child.search_permutations(remaining_phones)

    def assemble(self):
        '''Aggregate all phones up the trie from this node, inclusive. Returns a generator'''
        if self.phone:
            yield self.phone
            yield from self.parent.assemble()

    def count_nodes(self):
        '''Counts the number of nodes in the trie'''
        return 1 + sum(child.count_nodes() for child in self.children.values())

    def count_words(self):
        '''Counts the number of words in the trie'''
        return len(self.words) + sum(child.count_words() for child in self.children.values())

    def get_sub_words(self):
        yield from self.words
        for child in self.children.values():
            yield from child.get_sub_words()

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
                for consonant in CONSONANTS:
                    # try all permutations with this added consonant
                    child = self.children.get(consonant)
                    if child:
                        yield from child.search_permutations(phones)
