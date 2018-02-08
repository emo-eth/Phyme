'''Utils related to rhyming'''
import IOUtil

phone_type_dict, type_phone_dict = IOUtil.load_phone_type_dicts()
word_phone_dict = IOUtil.load_word_phone_dict()


def is_vowel(phone):
    '''Given a phone, determine if it is a vowel'''
    return phone_type_dict[phone] == 'vowel'


def extract_syllables(phones):
    '''Extract syllable groupings from a list of phones. Syllables are split by
    vowel, including ending consonants. Leading consonants are grouped with
    the following vowel and consonants (eg DOG -> [[D, AH1, G]])
    Returns a list of lists of string phones'''
    syllables = []
    syllable = []
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


def get_last_stressed(word):
    '''
    Gets the last stressed syllable of a word, and any unstressed syllables
    following it.
    Returns a list of lists of string phones.
    '''
    word = word.upper()
    phones = word_phone_dict[word]
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
    if is_vowel(phone_type_dict[syllable[0]]):
        vowel = syllable[0]
    else:
        vowel = syllable[1]
    return vowel[-1] == '1' or vowel[-1] == '2'
