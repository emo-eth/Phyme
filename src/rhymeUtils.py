'''Utils related to rhyming'''
import IOUtil
from util import flatten
from collections import defaultdict

STRESSED_FLAGS = {'1', '2'}
VOICED_CONSONANTS = {'B', 'D', 'G', 'V', 'DH', 'Z', 'ZH', 'JH', 'M', 'N', 'NG',
                     'L', 'R'}

phone_type_dict, type_phone_dict = IOUtil.load_phone_type_dicts()
word_phone_dict = IOUtil.load_word_phone_dict()
type_voiced_phone_dict = defaultdict(lambda: defaultdict(set))


def is_voiced(phone):
    '''Given a phone, determine if it is voiced
    Returns a boolean'''
    return phone in VOICED_CONSONANTS or is_vowel(phone)


def is_vowel(phone):
    '''
    Given a phone, determine if it is a vowel
    Returns a boolean
    '''
    return phone_type_dict[phone] == IOUtil.VOWEL


def extract_syllables(phones):
    '''Extract syllable groupings from a list of phones. Syllables are split by
    vowel, including ending consonants. Leading consonants are grouped with
    the following vowel and consonants (eg DOG -> [[D, AH1, G]])
    Returns a list of lists of string phones'''
    syllables = []
    syllable = []
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


def get_last_stressed(phones, num_sylls=1):
    '''
    Gets the last stressed syllable of a list of phones, and any unstressed
    syllables following it.
    TODO: import getting a certain number of syllables
    TODO: distinct from getting x num of syllables?
    Returns a list of lists of string phones.
    '''
    syllables = extract_syllables(phones)
    if len(syllables) == 1:
        return syllables
    if is_stressed(syllables[-1]):
        return [syllables[-1]]
    else:
        return syllables[-2:]


def is_stressed(syllable):
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


def is_consonant(phone):
    '''
    Determine if a phone is a consonant
    Returns a boolean
    '''
    return phone_type_dict[phone] != IOUtil.VOWEL


def get_consonant_family(consonant):
    '''Given a consonant, get its family (type, voiced) members'''
    family = phone_type_dict[consonant]
    return type_voiced_phone_dict[family][is_voiced(consonant)]


def get_consonant_partners(consonant):
    '''Given a consonant, get its type members'''
    family = phone_type_dict[consonant]
    return type_phone_dict[family]


def get_last_syllable(word, num_sylls=1):
    word = word.upper()
    phones = word_phone_dict[word]
    # TODO: support multi-syllable-rhymes
    phones = list(flatten(get_last_stressed(phones, num_sylls)))
    if is_consonant(phones[0]):
        phones = phones[1:]
    return phones


def get_phones(word):
    return word_phone_dict[word.upper()]

# TODO: move this to IOUtil? But depends on is_voiced fn
for type_, phones in type_phone_dict.items():
    for phone in phones:
        if is_voiced(phone):
            type_voiced_phone_dict[type_][True].add(phone)
        else:
            type_voiced_phone_dict[type_][False].add(phone)
