'''Utils for loading and parsing pronunciation data into data structures'''
from collections import defaultdict
from RhymeTrie import RhymeTrie
import os

file_path = os.path.dirname(__file__)

AFFRICATE = 'affricate'
FRICATIVE = 'fricative'

# use global objects so we don't load data each time we call a method
rt = None
word_phone_dict = {}
phone_type_dict = {}
type_phone_dict = defaultdict(set)


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


def load_word_phone_dict():
    '''Load a dict of word -> phones mappings'''
    if word_phone_dict:
        return word_phone_dict
    # associate words with a list of phonemes
    with open(os.path.join(file_path, '../cmudict/cmudict-0.7b.txt'),
              encoding='latin1') as f:
        for line in f:
            if line.startswith(';;;'):
                continue
            splits = line.split()
            word = splits[0]
            word_phone_dict[splits[0]] = splits[1:]
    return word_phone_dict


def load_phone_type_dicts():
    '''Load both phone -> type and type -> phone mapped dicts'''
    if phone_type_dict and type_phone_dict:
        return phone_type_dict, type_phone_dict
    with open(os.path.join(file_path, '../cmudict/cmudict-0.7b.phones.txt'),
              encoding='latin1') as f:
        for line in f:
            phone, family = line.split()
            # at the expense of linguistic purity, group affricates and
            # fricatives together for rhyming purposes
            if family == AFFRICATE:
                family = FRICATIVE
            phone_type_dict[phone] = family
            if family == 'vowel':
                # quick lookup for stressed syllables: AY0, AY1, AY2
                for x in range(3):
                    phone_type_dict[phone + str(x)] = 'vowel'
            type_phone_dict[family].add(phone)
    return phone_type_dict, type_phone_dict
