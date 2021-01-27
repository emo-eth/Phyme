

from typing import Dict, FrozenSet, List


Phone = str
PhoneType = str
Syllable = List[Phone]
PhymeResult = Dict[int, List[str]]

STRESSED_FLAGS: FrozenSet[Phone] = frozenset(('1', '2'))
VOICED_CONSONANTS: FrozenSet[Phone] = frozenset(('B', 'D', 'G', 'V', 'DH', 'Z', 'ZH', 'JH', 'M',
                               'N', 'NG', 'L', 'R'))
AFFRICATE: PhoneType = 'affricate'
FRICATIVE: PhoneType = 'fricative'
VOWEL: PhoneType = 'vowel'