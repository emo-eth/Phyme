import unittest
import sys

sys.path.append('../')
from Phyme import rhymeUtils as ru
# from Phyme.rhymeUtils import RhymeUtils, PhoneUtils
PhoneUtils = ru.PhoneUtils
RhymeUtils = ru.RhymeUtils


class RhymeUtilsTest(unittest.TestCase):

    def test_get_phones(self):
        # get_phones returns correct (number of) phones
        self.assertEqual(len(PhoneUtils.get_phones('dog')), 3)
        self.assertEqual(len(PhoneUtils.get_phones('a')), 1)

    def test_extract_syllables(self):
        # extract_syllables returns correct number of syllables
        dog = PhoneUtils.get_phones('dog')
        dog_sylls = PhoneUtils.extract_syllables(dog)
        self.assertEquals(len(dog_sylls), 1)
        anti = PhoneUtils.get_phones('antidisestablishmentarianism')
        anti_sylls = PhoneUtils.extract_syllables(anti)
        self.assertEquals(len(anti_sylls), 12)

    def test_is_voiced(self):
        # is_voiced distinguishes between un/voiced consonants. vowels are voiced
        self.assertTrue(RhymeUtils._is_voiced('JH'))
        self.assertTrue(RhymeUtils._is_voiced('Z'))
        self.assertFalse(RhymeUtils._is_voiced('CH'))
        self.assertTrue(RhymeUtils._is_voiced('AY'))

    def test_get_last_stressed(self):
        # test get_last_stressed gets the last stressed syllable and following unstressed
        anti = PhoneUtils.get_phones('antidisestablishmentarianism')
        stressed = PhoneUtils.get_last_stressed(PhoneUtils.extract_syllables(anti))
        self.assertEqual(len(stressed), 2)
        begin = PhoneUtils.get_phones('begin')
        stressed = PhoneUtils.get_last_stressed(PhoneUtils.extract_syllables(begin))
        self.assertEqual(len(stressed), 1)

    def test_is_vowel(self):
        self.assertTrue(RhymeUtils._is_vowel('AY'))
        self.assertFalse(RhymeUtils._is_vowel('ZH'))

    def test_is_consonant(self):
        self.assertTrue(RhymeUtils._is_consonant('ZH'))
        self.assertFalse(RhymeUtils._is_consonant('AY'))

    def test_is_stressed(self):
        self.assertTrue(PhoneUtils.is_stressed([ru.Phone('AY1')]))
        self.assertTrue(PhoneUtils.is_stressed([ru.Phone('AY2')]))
        self.assertFalse(PhoneUtils.is_stressed([ru.Phone('AY0')]))

    def test_get_consonant_family(self):
        self.assertTrue('ZH' in RhymeUtils.get_consonant_family('Z'))

    def get_consonant_partners(self):
        self.assertTrue('CH' in RhymeUtils.get_consonant_partners('JH'))

    def test_strip_leading_consonants(self):
        phones = PhoneUtils.get_phones('frog')
        stripped = PhoneUtils.strip_leading_consonants(phones)
        self.assertTrue(stripped[0].is_vowel)


if __name__ == '__main__':
    unittest.main()
