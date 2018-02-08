'''Utils related to rhyming'''
import IOUtil

VOWEL = 'vowel'
STRESSED_FLAGS = {'1', '2'}

phone_type_dict, type_phone_dict = IOUtil.load_phone_type_dicts()
word_phone_dict = IOUtil.load_word_phone_dict()


def is_vowel(phone):
    '''
    Given a phone, determine if it is a vowel
    Returns a boolean
    '''
    return phone_type_dict[phone] == VOWEL


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


def get_last_stressed(phones):
    '''
    Gets the last stressed syllable of a list of phones, and any unstressed
    syllables following it.
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
    return phone_type_dict[phone] != VOWEL


def flatten(x):
    '''Generator of values from a 2d collection'''
    for y in x:
        yield from y
