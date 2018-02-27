from RhymeTrieNode import RhymeTrieNode


class RhymeTrie(object):
    '''A RhymeTrie holds RhymeTrie nodes and accesses them.'''
    
    def __init__(self):
        self.children = {}
    
    def insert(self, phones, word):
        '''Given a word and its phones, insert them into the trie. Associate the word with the end node.
        Returns a RhymeTrieNode'''
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
        
    def count_nodes(self):
        '''Counts the number of children nodes in the trie'''
        return sum(child.count_nodes() for _, child in self.children.items())
    
    def count_words(self):
        '''Counts the number of words in the trie'''
        return sum(child.count_words() for _, child in self.children.items())