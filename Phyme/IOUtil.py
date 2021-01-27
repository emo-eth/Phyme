'''Utils for loading and parsing pronunciation data into data structures'''
from .constants import StringPhone, PhoneType
import json
import os
from typing import Dict


file_path = os.path.dirname(__file__)

# use global objects so we don't load data each time we call a method
word_phone_dict: Dict[str, StringPhone] = {}
phone_type_dict: Dict[StringPhone, PhoneType] = {}
type_phone_dict: Dict[PhoneType, StringPhone] = {}
# type_voiced_phone_dict: Dict[] = defaultdict(lambda: defaultdict(set))


def load_word_phone_dict():
    '''Load a dict of word -> phones mappings'''
    if word_phone_dict:
        return word_phone_dict
    with open(os.path.join(file_path, 'data/word_phone.json')) as f:
        word_phone_dict.update(json.load(f))
    return word_phone_dict


def load_phone_type_dicts():
    '''Load both phone -> type and type -> phone mapped dicts'''
    if phone_type_dict and type_phone_dict:
        return phone_type_dict, type_phone_dict
    with open(os.path.join(file_path, 'data/phone_type.json')) as f:
        phone_type_dict.update(json.load(f))
    with open(os.path.join(file_path, 'data/type_phone.json')) as f:
        type_phone_dict.update(json.load(f))
    return phone_type_dict, type_phone_dict
