'''Utils related to rhyming'''
from .util import Phone, PhoneType, Syllable
from . import IOUtil
from collections import defaultdict
from enum import Enum
from typing import Callable, Dict, Iterable, List, Set, Union

def _auto():
    count = 0
    while True:
        yield count
        count += 1


STRESSED_FLAGS = frozenset(('1', '2'))
VOICED_CONSONANTS = frozenset(('B', 'D', 'G', 'V', 'DH', 'Z', 'ZH', 'JH', 'M',
                               'N', 'NG', 'L', 'R'))
AFFRICATE = 'affricate'
FRICATIVE = 'fricative'
VOWEL = 'vowel'

phone_type_dict, type_phone_dict = IOUtil.load_phone_type_dicts()
word_phone_dict = IOUtil.load_word_phone_dict()
type_voiced_phone_dict: Dict[PhoneType, Dict[bool, Set[Phone]]] = defaultdict(lambda: defaultdict(set))


class MetaPhone(object):
    def __init__(self, phone: Phone, replacement_phones: List[Phone]):
        self.phone = phone
        self.replacement_phones = set([phone]).union(set(replacement_phones))

    def __equals__(self, other):
        if isinstance(other, str):
            return other in self.replacement_phones
        elif isinstance(other, MetaVowel):
            return len(self.replacement_phones.union(other.replacement_phones)) != 0

class MetaVowel(MetaPhone):
    pass

# TODO: meta consonants, as in interchangeable phonemes?
# eg: draft becoming jraft
class MetaConsonant(MetaPhone):
    pass

class PermutedPhone(object):

    def __init__(self, phone: Phone, permutation: 'Permutation'):
        self.phone = phone
        self.permutation = permutation

    def __repr__(self):
        return self.phone + ' ' + self.permutation.name


class Permutation(Enum):
    ADDITIVE = _auto()
    SUBTRACTIVE = _auto()
    PARTNER = _auto()
    FAMILY = _auto()
    ASSONANCE = _auto()
    CONSONANT = _auto()
    SUBSTITUTION = _auto()


def permuted_phone_mapper(permutation: Permutation,
                          test: Callable[[Phone], bool]) -> Callable[[Phone], Union[Phone, PermutedPhone]]:
    return lambda x: PermutedPhone(phone, permutation) if test(phone) else phone

def is_vowel(phone: Union[Phone, PermutedPhone]) -> bool:
    '''
    Given a phone, determine if it is a vowel
    Returns a boolean
    '''
    if isinstance(phone, PermutedPhone):
        phone = phone.phone
    return phone_type_dict.get(phone) == VOWEL


def is_consonant(phone: Union[Phone, PermutedPhone]):
    '''
    Determine if a phone is a consonant
    Returns a boolean
    '''
    return not is_vowel(phone)


CONSONANTS = frozenset(x for x in phone_type_dict if is_consonant(x))
VOWELS = frozenset(x for x in phone_type_dict if is_vowel(x))


def is_voiced(phone):
    '''Given a phone, determine if it is voiced
    Returns a boolean'''
    return phone in VOICED_CONSONANTS or is_vowel(phone)


def extract_syllables(phones: List[Phone]) -> List[Syllable]:
    '''Extract syllable groupings from a list of phones. Syllables are split by
    vowel, including ending consonants. Leading consonants are grouped with
    the following vowel and consonants (eg DOG -> [[D, AH1, G]])
    Returns a list of lists of string phones'''
    syllables: List[Syllable] = []
    syllable: Syllable = []
    # keep track of whether or not we have seen an initial vowel
    seen_vowel = False
    for phone in phones:
        if is_vowel(phone):
            if syllable and seen_vowel:
                syllables.append(syllable)
                syllable = []
            seen_vowel = True
        syllable.append(phone)
    syllables.append(syllable)
    return syllables


def count_syllables(word:str):
    phones = get_phones(word)
    return len(extract_syllables(phones))


def get_last_stressed(syllables: List[Syllable]):
    '''
    Gets the last stressed syllable of a list of phones, and any unstressed
    syllables following it.
    TODO: import getting a certain number of syllables
    TODO: distinct from getting x num of syllables?
    Returns a list of lists of string phones.
    '''
    if len(syllables) == 1:
        return syllables
    if is_stressed(syllables[-1]):
        return syllables[-1:]
    else:
        return syllables[-2:]


def is_stressed(syllable: Syllable):
    '''
    Tests if a syllable (list of string phones) is stressed
    Returns a boolean
    '''
    # first syllable may have a leading consonant
    if is_vowel(syllable[0]):
        vowel = syllable[0]
    else:
        vowel = syllable[1]
    return vowel[-1] in STRESSED_FLAGS


def get_consonant_family(consonant: Phone):
    '''Given a consonant, get its family (type, voiced) members'''
    family = phone_type_dict[consonant]
    return type_voiced_phone_dict[family][is_voiced(consonant)]


def get_consonant_partners(consonant):
    '''Given a consonant, get its type members'''
    family = phone_type_dict[consonant]
    return type_phone_dict[family]


def get_last_syllables(word:str, num_sylls: int=-1) -> List[Syllable]:
    # TODO: care about stresses?
    word = word.upper()
    phones = word_phone_dict[word]
    syllables = extract_syllables(phones)
    if num_sylls == -1:
        syllables = get_last_stressed(syllables)
    else:
        syllables = syllables[-num_sylls:]
    syllables[0] = strip_leading_consonants(syllables[0])
    return syllables


def strip_leading_consonants(phones) -> List[Phone]:
    for i, phone in enumerate(phones):
        if is_vowel(phone):
            return phones[i:]
    return phones


def get_phones(word: str) -> List[Phone]:
    return word_phone_dict[word.upper()]


# TODO: move this to IOUtil? But depends on is_voiced fn
for type_, phones in type_phone_dict.items():
    for phone in phones:
        if is_voiced(phone):
            type_voiced_phone_dict[type_][True].add(phone)
        else:
            type_voiced_phone_dict[type_][False].add(phone)

permutation_getters: Dict[Permutation, Callable[[Phone], Iterable[Phone]]] = {
    Permutation.ADDITIVE: lambda x: [x],
    Permutation.SUBTRACTIVE: lambda x: [x],
    Permutation.PARTNER: get_consonant_partners,
    Permutation.FAMILY: get_consonant_family,
    Permutation.ASSONANCE: lambda x: [x],
    Permutation.CONSONANT: lambda _: VOWELS,
    Permutation.SUBSTITUTION: lambda _: CONSONANTS
}
