'''Utils for loading and parsing pronunciation data into data structures'''
from .constants import StringPhone, PhoneType
import json
import os
from typing import Dict, List, Set, Tuple


__file_path = os.path.dirname(__file__)

# use global objects so we don't load data each time we call a method
_word_phone_dict: Dict[str, List[StringPhone]] = {}
_phone_type_dict: Dict[StringPhone, PhoneType] = {}
_type_phone_dict: Dict[PhoneType, Set[StringPhone]] = {}


def load_word_phone_dict() -> Dict[str, List[StringPhone]]:
    '''Load a dict of word -> phones mappings'''
    if _word_phone_dict:
        return _word_phone_dict
    with open(os.path.join(__file_path, 'data/word_phone.json')) as f:
        _word_phone_dict.update(json.load(f))
    return _word_phone_dict


def load_phone_type_dicts() -> Tuple[Dict[StringPhone, PhoneType], Dict[PhoneType, Set[StringPhone]]]:
    '''Load both phone -> type and type -> phone mapped dicts'''
    if _phone_type_dict and _type_phone_dict:
        return _phone_type_dict, _type_phone_dict
    with open(os.path.join(__file_path, 'data/phone_type.json')) as f:
        _phone_type_dict.update(json.load(f))
    with open(os.path.join(__file_path, 'data/type_phone.json')) as f:
        _type_phone_dict.update(json.load(f))
    return _phone_type_dict, _type_phone_dict
