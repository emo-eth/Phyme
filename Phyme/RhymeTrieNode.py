from typing import Dict, Iterable, List, Optional, Sequence, Set, Type, Union

from Phyme.constants import StringPhone
from Phyme.rhymeUtils import MetaPhone, PermutedPhone, Permutation, Phone


class RhymeTrieNode(object):
    def __init__(self, phone: Optional[Phone], parent: Optional["RhymeTrieNode"]):
        self.children: Dict[Phone, RhymeTrieNode] = {}
        self.parent: Optional[RhymeTrieNode] = parent
        self.phone: Optional[Phone] = phone
        self.words: Set[str] = set()

    def insert(self, phones: List[Phone], word: str) -> "RhymeTrieNode":
        """Insert a list of phones into this node and its children. Returns the final node of the insert."""
        if not phones:
            self.words.add(word.lower())
            return self
        child_node = self.children.get(phones[0])
        if child_node is None:
            child_node = RhymeTrieNode(phones[0], self)
            self.children[phones[0]] = child_node
        remaining_phones = phones[1:]
        return child_node.insert(remaining_phones, word)

    def contains(self, phones: List[Phone]) -> Union["RhymeTrieNode", bool]:
        """Given a list of phones, finds the end node in the trie associated with those phones.
        Returns a RhymeTrieNode or False if there is no end node associated with the given phones"""
        if phones:
            child_node = self.children.get(phones[0])
            if child_node:
                search_results = child_node.search(phones[1:])
                return search_results if search_results is not None else False
        elif self.words:
            return self
        return False

    def search(self, phones: List[Phone]) -> Optional["RhymeTrieNode"]:
        """Given a list of phones, find a node in the trie associated with those phones.
        Returns a RhymeTrieNode or None if there is no node associated with the given phones"""
        if not phones:
            return self
        child_node = self.children.get(phones[0])
        if child_node:
            return child_node.search(phones[1:])
        return None

    def search_permutations(
        self, phones: List[Union[Phone, PermutedPhone]]
    ) -> Iterable["RhymeTrieNode"]:
        """Returns a generator of nodes"""
        if not phones:
            yield self
            return
        yield from self._replace_phones(phones)
        yield from self._add_subtract_phones(phones)
        permuted_phones = self._get_permuted_phones(phones[0])
        remaining_phones = phones[1:]
        for phone in permuted_phones:
            child = self.children.get(phone)
            if child:
                yield from child.search_permutations(remaining_phones)

    def assemble(self) -> Iterable[StringPhone]:
        """Aggregate all phones up the trie from this node, inclusive. Returns a generator"""
        if self.phone:
            yield self.phone.phone
            assert self.parent is not None
            yield from self.parent.assemble()

    def count_nodes(self) -> int:
        """Counts the number of nodes in the trie"""
        return 1 + sum(child.count_nodes() for child in self.children.values())

    def count_words(self) -> int:
        """Counts the number of words in the trie"""
        return len(self.words) + sum(
            child.count_words() for child in self.children.values()
        )

    def get_sub_words(self) -> Iterable[str]:
        yield from self.words
        for child in self.children.values():
            yield from child.get_sub_words()

    def _get_permuted_phones(
        self, phone: Union[Phone, PermutedPhone]
    ) -> Iterable[Phone]:
        if isinstance(phone, PermutedPhone):
            yield from phone.permutation.apply(phone.phone)
        else:
            yield phone

    def _add_subtract_phones(
        self, phones: List[Union[Phone, PermutedPhone]]
    ) -> Iterable["RhymeTrieNode"]:
        if isinstance(phones[0], PermutedPhone):
            phone = phones[0]
            # try all permutations without this phone
            if phone.permutation == Permutation.SUBTRACTIVE:
                yield from self.search_permutations(phones[1:])
            elif phone.permutation == Permutation.ADDITIVE:
                for consonant in Phone.CONSONANTS:
                    # try all permutations with this added consonant
                    child = self.children.get(consonant)
                    if child:
                        yield from child.search_permutations(phones)

    def _replace_phones(
        self, phones: List[Union[Phone, PermutedPhone]]
    ) -> Iterable["RhymeTrieNode"]:
        first_phone = phones[0]
        remaining_phones = phones[1:]
        if isinstance(first_phone, MetaPhone):
            for phone in first_phone.replacement_phones:
                # TODO: MetaPermutedPhone?
                new_phone: List[Union[Phone, PermutedPhone]] = [Phone(phone.phone)]
                new_phones: List[Union[Phone, PermutedPhone]] = (
                    new_phone + remaining_phones
                )
                yield from self.search_permutations(new_phones)
