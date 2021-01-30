'''Utils for loading and parsing pronunciation data into data structures'''
from .constants import StringPhone, PhoneType
import json
import os
from typing import Dict, List, Optional, Set


_file_path = os.path.dirname(__file__)


class IOUtil(object):
    _word_phone_dict: Optional[Dict[str, List[StringPhone]]] = None
    _phone_type_dict: Optional[Dict[StringPhone, PhoneType]] = None
    _type_phone_dict: Optional[Dict[PhoneType, Set[StringPhone]]] = None

    @staticmethod
    def load_word_phone_dict() -> Dict[str, List[StringPhone]]:
        '''Load a dict of word -> phones mappings'''
        if IOUtil._word_phone_dict:
            return IOUtil._word_phone_dict
        with open(os.path.join(_file_path, 'data/word_phone.json')) as f:
            IOUtil._word_phone_dict = json.load(f)

        assert IOUtil._word_phone_dict is not None
        return IOUtil._word_phone_dict

    @staticmethod
    def _load_phone_type_dicts():
        '''Load both phone -> type and type -> phone mapped dicts'''
        if IOUtil._phone_type_dict and IOUtil._type_phone_dict:
            return
        with open(os.path.join(_file_path, 'data/phone_type.json')) as f:
            IOUtil._phone_type_dict = (json.load(f))
        with open(os.path.join(_file_path, 'data/type_phone.json')) as f:
            IOUtil._type_phone_dict = (json.load(f))

    @staticmethod
    def load_type_phone_dict():
        IOUtil._load_phone_type_dicts()
        assert IOUtil._type_phone_dict is not None
        return IOUtil._type_phone_dict

    @staticmethod
    def load_phone_type_dict():
        IOUtil._load_phone_type_dicts()
        assert IOUtil._phone_type_dict is not None
        return IOUtil._phone_type_dict
