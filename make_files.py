import json
import pickle
import os
import sys
from collections import defaultdict
from typing import Dict, List

from Phyme.util import Phone, PhoneType

file_path = os.path.dirname(__file__)

AFFRICATE = 'affricate'
FRICATIVE = 'fricative'
VOWEL = 'vowel'


def load_word_phone_dict() -> Dict[str, List[Phone]]:
    '''Load a dict of word -> phones mappings'''
    word_phone_dict = dict()
    with open(os.path.join(file_path, 'cmudict/cmudict-0.7b.txt'),
              encoding='latin1') as f:
        for line in f:
            if line.startswith(';;;'):
                continue
            splits = line.split()
            word = splits[0]
            word_phone_dict[word] = splits[1:]
    return word_phone_dict


def load_phone_type_dicts():
    '''Load both phone -> type and type -> phone mapped dicts'''
    phone_type_dict: Dict[Phone, PhoneType] = dict()
    type_phone_dict: Dict[PhoneType, Dict[Phone, Phone]] = defaultdict(dict)
    with open(os.path.join(file_path, 'cmudict/cmudict-0.7b.phones.txt'),
              encoding='latin1') as f:
        for line in f:
            phone, family = line.split()
            # at the expense of linguistic purity, group affricates and
            # fricatives together for rhyming purposes
            if family == AFFRICATE:
                family = FRICATIVE
            phone_type_dict[phone] = family
            if family == VOWEL:
                # quick lookup for stressed syllables: AY0, AY1, AY2
                for x in range(3):
                    stressed_phone = phone + str(x)
                    phone_type_dict[stressed_phone] = family
                    type_phone_dict[family][stressed_phone] = stressed_phone
            type_phone_dict[family][phone] = phone
    return phone_type_dict, type_phone_dict


def load_type_voiced_phone_dict():
    from Phyme.rhymeUtils import is_voiced
    _, type_phone_dict = load_phone_type_dicts()
    type_voiced_phone_dict: Dict[PhoneType, Dict[bool, Dict[Phone, Phone]]] = defaultdict(lambda: defaultdict(dict))
    for type_, phones in type_phone_dict.items():
        for phone in phones:
            if is_voiced(phone):
                type_voiced_phone_dict[type_][True][phone] = phone
            else:
                type_voiced_phone_dict[type_][False][phone] = phone
    return type_voiced_phone_dict


def load_rhyme_trie():
    '''Load a fully-loaded RhymeTrie object'''
    from Phyme.RhymeTrieNode import RhymeTrieNode
    word_phone_dict = load_word_phone_dict()
    rt = RhymeTrieNode(None, None)
    for word, phones in word_phone_dict.items():
        rt.insert(phones[::-1], word)
    return rt


def write_json():
    word_phone_dict = load_word_phone_dict()
    with open('Phyme/data/word_phone.json', 'w') as f:
        json.dump(word_phone_dict, f)
    phone_type_dict, type_phone_dict = load_phone_type_dicts()
    with open('Phyme/data/phone_type.json', 'w') as f:
        json.dump(phone_type_dict, f)
    with open('Phyme/data/type_phone.json', 'w') as f:
        json.dump(type_phone_dict, f)


def write_dependent_json():
    type_voiced_phone_dict = load_type_voiced_phone_dict()
    with open('Phyme/data/type_voiced_phone.json', 'w') as f:
        json.dump(type_voiced_phone_dict, f)


def write_pickle():
    rt = load_rhyme_trie()
    with open('Phyme/data/RhymeTrie.pkl', 'wb') as f:
        pickle.dump(rt, f)


def main():
    write_json()
    write_dependent_json()
    write_pickle()



if __name__ == '__main__':
    main()
