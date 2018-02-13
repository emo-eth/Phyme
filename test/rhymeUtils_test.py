import unittest
import sys
sys.path.append('../src')
import rhymeUtils as ru


class RhymeUtilsTest(unittest.TestCase):

    def test_get_phones(self):
        # get_phones returns correct (number of) phones
        self.assertEqual(len(ru.get_phones('dog')), 3)
        self.assertEqual(len(ru.get_phones('a')), 1)

    def test_extract_syllables(self):
        # extract_syllables returns correct number of syllables
        dog = ru.get_phones('dog')
        dog_sylls = ru.extract_syllables(dog)
        self.assertEquals(len(dog_sylls), 1)
        anti = ru.get_phones('antidisestablishmentarianism')
        anti_sylls = ru.extract_syllables(anti)
        self.assertEquals(len(anti_sylls), 12)

    def test_is_voiced(self):
        # is_voiced distinguishes between un/voiced consonants. vowels are voiced
        self.assertTrue(ru.is_voiced('JH'))
        self.assertTrue(ru.is_voiced('Z'))
        self.assertFalse(ru.is_voiced('CH'))
        self.assertTrue(ru.is_voiced('AY'))

    def test_get_last_stressed(self):
        # test get_last_stressed gets the last stressed syllable and following unstressed
        anti = ru.get_phones('antidisestablishmentarianism')
        stressed = ru.get_last_stressed(anti, num_sylls=1)
        self.assertEqual(len(stressed), 2)
        begin = ru.get_phones('begin')
        stressed = ru.get_last_stressed(begin, num_sylls=1)
        self.assertEqual(len(stressed), 1)

    def test_is_vowel(self):
        self.assertTrue(ru.is_vowel('AY'))
        self.assertFalse(ru.is_vowel('ZH'))

    def test_is_consonant(self):
        self.assertTrue(ru.is_consonant('ZH'))
        self.assertFalse(ru.is_consonant('AY'))

    def test_is_stressed(self):
        self.assertTrue(ru.is_stressed(['AY1']))
        self.assertTrue(ru.is_stressed(['AY2']))
        self.assertFalse(ru.is_stressed(['AY0']))

    def test_get_consonant_family(self):
        self.assertTrue('ZH' in ru.get_consonant_family('Z'))

    def get_consonant_partners(self):
        self.assertTrue('CH' in ru.get_consonant_partners('JH'))

if __name__ == '__main__':
    unittest.main()
