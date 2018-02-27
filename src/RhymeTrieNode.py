class RhymeTrieNode(object):

    def __init__(self, phone, parent):
        self.children = {}
        self.parent = parent
        self.phone = phone
        self.words = set()

    def insert(self, phones):
        '''Insert a list of phones into this node and its children. Returns the final node of the insert.'''
        if not phones:
            return self
        child_node = self.children.get(phones[0])
        if child_node is None:
            child_node = RhymeTrieNode(phones[0], self)
            self.children[phones[0]] = child_node
        remaining_phones = phones[1:]
        return child_node.insert(remaining_phones)

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

    def assemble(self):
        '''Aggregate all phones up the trie from this node, inclusive. Returns a generator'''
        if isinstance(self.parent, RhymeTrieNode):
            yield self.phone
            yield from self.parent.assemble()
        else:
            yield self.phone

    def count_nodes(self):
        '''Counts the number of children nodes in the trie'''
        return 1 + sum(child.count_nodes() for child in self.children.values())

    def count_words(self):
        '''Counts the number of words in the trie'''
        return len(self.words) + sum(child.count_words() for child in self.children.values())

    def get_sub_words(self):
        yield from self.words
        for _, child in self.children.items():
            yield from child.get_sub_words()
