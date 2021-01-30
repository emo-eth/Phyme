'''Utils related to rhyming'''
from .IOUtil import IOUtil
from .constants import StringPhone, PhoneType, STRESSED_FLAGS, VOICED_CONSONANTS, VOWEL
from collections import defaultdict
from enum import Enum
from typing import Callable, Dict, FrozenSet, Iterable, List, Optional, Set, Tuple, Type, TypeVar, Union


class RhymeUtils(object):

    CONSONANTS: FrozenSet[StringPhone]
    VOWELS: FrozenSet[StringPhone]

    _phone_type_dict = IOUtil.load_phone_type_dict()
    _type_phone_dict = IOUtil.load_type_phone_dict()
    _word_phone_dict = IOUtil.load_word_phone_dict()
    _type_voiced_phone_dict: Dict[PhoneType, Dict[bool, Set[StringPhone]]] = defaultdict(
        lambda: defaultdict(set))

    @staticmethod
    def _is_vowel(phone: StringPhone) -> bool:
        '''
        Given a phone, determine if it is a vowel
        Returns a boolean
        '''
        return RhymeUtils._phone_type_dict.get(phone) == VOWEL

    @staticmethod
    def _is_consonant(phone: StringPhone):
        '''
        Determine if a phone is a consonant
        Returns a boolean
        '''
        return not RhymeUtils._is_vowel(phone)

    @staticmethod
    def get_consonant_family(consonant: StringPhone):
        '''Given a consonant, get its family (type, voiced) members'''
        family = RhymeUtils._phone_type_dict.get(consonant)
        return RhymeUtils._type_voiced_phone_dict[family][RhymeUtils._is_voiced(consonant)]

    @staticmethod
    def get_consonant_partners(consonant):
        '''Given a consonant, get its type members'''
        family = RhymeUtils._phone_type_dict.get(consonant)
        return RhymeUtils._type_phone_dict.get(family)

    @staticmethod
    def _is_voiced(phone: StringPhone):
        '''Given a phone, determine if it is voiced
        Returns a boolean'''
        return phone in VOICED_CONSONANTS or RhymeUtils._is_vowel(phone)


for _type, _phones in RhymeUtils._type_phone_dict.items():
    for _phone in _phones:
        if RhymeUtils._is_voiced(_phone):
            RhymeUtils._type_voiced_phone_dict[_type][True].add(_phone)
        else:
            RhymeUtils._type_voiced_phone_dict[_type][False].add(_phone)
RhymeUtils.CONSONANTS = frozenset(
    x for x in RhymeUtils._phone_type_dict.keys() if RhymeUtils._is_consonant(x))
RhymeUtils.VOWELS = frozenset(
    x for x in RhymeUtils._phone_type_dict.keys() if RhymeUtils._is_vowel(x))


class UnknownPronunciationException(KeyError):

    def __init__(self, word):
        self.message = 'Word "{word}" is not in the loaded pronunciation dictionary.'.format(
            word=word)
        super().__init__(self)


class Phone(object):

    VOWELS: FrozenSet['Phone']
    CONSONANTS: FrozenSet['Phone']

    def __init__(self, phone: StringPhone):
        self.phone = phone
        self.is_vowel = self._is_vowel(phone)
        self.is_consonant = self._is_consonant(phone)
        self.is_voiced = self._is_voiced(phone)
        self.family = RhymeUtils._phone_type_dict.get(phone)

    def get_consonant_family_members(self) -> Optional[Set['Phone']]:
        # necessary to return None? why not []? shouldn't get called anyway
        if self.is_vowel:
            return None
        assert self.family is not None
        # TODO: convenience method for these
        phones = RhymeUtils._type_voiced_phone_dict.get(
            self.family, {}).get(self.is_voiced)
        assert phones is not None
        return {Phone(phone) for phone in phones}

    def get_consonant_partners(self) -> Optional[Set['Phone']]:
        if self.is_vowel:
            return None
        assert self.family is not None
        phones = RhymeUtils._type_phone_dict.get(self.family)
        assert phones is not None
        return {Phone(phone) for phone in phones}

    # TODO: remove these?

    @staticmethod
    def _is_vowel(phone: StringPhone):
        return phone in RhymeUtils.VOWELS

    @staticmethod
    def _is_consonant(phone: StringPhone):
        return not RhymeUtils._is_vowel(phone)

    @staticmethod
    def _is_voiced(phone: StringPhone):
        return phone in VOICED_CONSONANTS or RhymeUtils._is_vowel(phone)

    def __str__(self):
        return self.phone

    def __repr__(self):
        return f'Phone[Vowel:{self.is_vowel}, Voiced:{self.is_voiced}, Phone: {self.phone}]'

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self.phone == other.phone
        elif isinstance(other, StringPhone):
            return self.phone == other
        return False

    def __hash__(self):
        return hash((self.phone, Phone))


Phone.VOWELS = frozenset(Phone(vowel) for vowel in RhymeUtils.VOWELS)
Phone.CONSONANTS = frozenset(Phone(consonant)
                             for consonant in RhymeUtils.CONSONANTS)


class ShortVowel(Phone):
    '''Eg leading w's and y's when they would otherwise add to syllable count'''

    def __init__(self, phone: StringPhone):
        super().__init__(phone)
        self.is_vowel = False
        self.is_consonant = False


class MetaPhone(Phone):

    def __init__(self, phone: Phone, *replacement_phones: Phone):
        super().__init__(phone.phone)
        self.replacement_phones = frozenset({phone, *replacement_phones})
        self.is_voiced = any(
            phone.is_voiced for phone in self.replacement_phones)

    def __str__(self):
        return '"' + self.phone + '"'

    def __repr__(self):
        return f'MetaPhone[Vowel:{self.is_vowel}, Voiced:{self.is_voiced}, Phones: {self.replacement_phones}>'

    def __eq__(self, other):
        if type(other) == StringPhone:
            return Phone(other) in self.replacement_phones
        elif type(other) == Phone:
            return other in self.replacement_phones
        elif isinstance(other, MetaPhone):
            return len(self.replacement_phones.intersection(other.replacement_phones)) > 0

    def __hash__(self):
        return super().__hash__()


class MetaVowel(MetaPhone):
    '''Useful for diphthongs and semivowels'''

    def __init__(self, phone: Phone, *replacement_phones: Phone):
        super().__init__(phone, *replacement_phones)
        self.is_vowel = True
        self.is_consonant = False

    def __repr__(self):
        return f'MetaVowel[Vowel:{self.is_vowel}, Voiced:{self.is_voiced}, Phones: {self.replacement_phones}>'

    def __hash__(self):
        return super().__hash__()


class MetaShortVowel(MetaPhone):
    def __init__(self, phone: ShortVowel, *replacement_phones: ShortVowel):
        super().__init__(phone, *replacement_phones)
        self.is_vowel = False
        self.is_consonant = False

    def __repr__(self):
        return f'MetaShortVowel[Vowel:{self.is_vowel}, Voiced:{self.is_voiced}, Phones: {self.replacement_phones}>'

    def __hash__(self):
        return super().__hash__()

# class CompoundMetaPhone(MetaPhone):
#     '''TODO: For replacing groups of phones with groups of phones?'''
#     def __init__(self, phone: List[Phone], *replacement_phones: List[Phone]):
#         super().__init__(phone, *replacement_phones)
#         self.is_vowel = True
#         self.is_consonant = False

#     def __repr__(self):
#         return f'MetaPhone[Vowel:{self.is_vowel}, Voiced:{self.is_voiced}, Phones: {self.replacement_phones}>'

#     def __hash__(self):
#         return super().__hash__()

# ExtendsPhone = TypeVar("ExtendsPhone", bound='Phone')
# ExtendsMetaPhone = TypeVar("ExtendsMetaPhone", bound=MetaPhone)


class PermutedPhone(object):

    def __init__(self, phone: Phone, permutation: 'Permutation'):
        self.phone = phone
        self.permutation = permutation

    def __repr__(self):
        return f'PermutedPhone[Permutation:{self.permutation.name}, {repr(self.phone)}]'

# TODO: test


class PermutedMetaPhone(object):

    def __init__(self, phone: Phone, permutation: 'Permutation'):
        self.phone = phone
        self.permutation = permutation

    def __repr__(self):
        return f'PermutedMetaPhone[Permutation:{self.permutation.name}, {repr(self.phone)}]'


# eg ending R's, or should it go ER -> A, (h)istoric?
class OptionalPhone(Phone):
    pass

# eg comfortable -> comftorbal. how to search when # of phones are different?


class ConsolidatedPhone(Phone):
    pass
# TODO: meta consonants, as in interchangeable phonemes?
# eg: draft becoming jraft
# probably unnecessary with MetaPhone


class MetaConsonant(MetaPhone):
    pass


Syllable = List[Phone]


class PhoneUtils(object):

    @staticmethod
    def is_stressed(syllable: Syllable) -> bool:
        '''
        Tests if a syllable (list of string phones) is stressed
        Returns a boolean
        '''
        # first syllable may have a leading consonant
        if syllable[0].is_vowel:
            vowel = syllable[0]
        else:
            vowel = syllable[1]
        return vowel.phone[-1] in STRESSED_FLAGS

    @staticmethod
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
        if PhoneUtils.is_stressed(syllables[-1]):
            return syllables[-1:]
        else:
            return syllables[-2:]

    @staticmethod
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
            if phone.is_vowel:
                if syllable and seen_vowel:
                    syllables.append(syllable)
                    syllable = []
                seen_vowel = True
            syllable.append(phone)
        syllables.append(syllable)
        return syllables

    @staticmethod
    def count_syllables(word: str):
        phones = PhoneUtils.get_phones(word)
        return len(PhoneUtils.extract_syllables(phones))

    @staticmethod
    def get_last_syllables(word: str, num_sylls: int = -1) -> List[Syllable]:
        # TODO: care about stresses?
        phones: List[Phone] = PhoneUtils.get_phones(word)
        if len(phones) == 0:
            raise UnknownPronunciationException(word)

        syllables = PhoneUtils.extract_syllables(phones)
        if num_sylls == -1:
            syllables = PhoneUtils.get_last_stressed(syllables)
        else:
            syllables = syllables[-num_sylls:]
        syllables[0] = PhoneUtils.strip_leading_consonants(syllables[0])
        return syllables

    @staticmethod
    def strip_leading_consonants(phones: List[Phone]) -> List[Phone]:
        for i, phone in enumerate(phones):
            if phone.is_vowel:
                return phones[i:]
        return phones

    @staticmethod
    def get_phones(word: str) -> List[Phone]:
        return [PhoneUtils.phone_mapper(phone) for phone in RhymeUtils._word_phone_dict.get(word.upper(), [])]

    @staticmethod
    def phone_mapper(phone: StringPhone) -> Phone:
        if phone == 'Y':
            # not MetaVowel because messes up syllable count?
            return MetaShortVowel(ShortVowel(phone), ShortVowel('IY0'))
        elif phone == 'W':
            return MetaShortVowel(ShortVowel(phone), ShortVowel('UW0'))
        return Phone(phone)


class Permutation(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, f: Callable[[Phone], Iterable[Phone]]):
        self.apply = f

    # ADDITIVE = lambda x: [x],
    # SUBTRACTIVE = lambda x: [x],
    # PARTNER = lambda phone: Phone.get_consonant_partners(phone),
    # FAMILY = lambda phone: Phone.get_consonant_family_members(phone),
    # CONSONANT = lambda _: Phone.VOWELS,
    # SUBSTITUTION = lambda _: Phone.CONSONANTS,

    ADDITIVE = lambda x: [x],
    SUBTRACTIVE = lambda x: [x],
    PARTNER = lambda phone: Phone.get_consonant_partners(phone),
    FAMILY = lambda phone: Phone.get_consonant_family_members(phone),
    CONSONANT = lambda _: Phone.VOWELS,
    SUBSTITUTION = lambda _: Phone.CONSONANTS,

    def map(self, test: Callable[[Phone], bool], iter: Iterable[Phone]) -> Iterable[Union[Phone, PermutedPhone]]:
        return map(lambda phone: PermutedPhone(phone, self) if test(phone) else phone, iter)
