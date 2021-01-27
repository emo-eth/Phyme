

from typing import Dict, FrozenSet, List


StringPhone = str
PhoneType = str
PhymeResult = Dict[int, List[str]]


STRESSED_FLAGS: FrozenSet[StringPhone] = frozenset(('1', '2'))
VOICED_CONSONANTS: FrozenSet[StringPhone] = frozenset(('B', 'D', 'G', 'V', 'DH', 'Z', 'ZH', 'JH', 'M',
                                                       'N', 'NG', 'L', 'R'))
AFFRICATE: PhoneType = 'affricate'
FRICATIVE: PhoneType = 'fricative'
VOWEL: PhoneType = 'vowel'
