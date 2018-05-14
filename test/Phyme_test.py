import unittest
import sys
sys.path.append('../src')
from Phyme import Phyme
from util import flatten


class PhymeTest(unittest.TestCase):
    rd = Phyme()

    def test_perfect_rhymes(self):
        self.assertTrue('COG' in flatten(self.rd.get_perfect_rhymes('dog').values()))
        self.assertTrue('OPAL' in flatten(self.rd.get_perfect_rhymes('constantinople').values()))

    def test_family_rhymes(self):
        self.assertTrue('FOB' in flatten(self.rd.get_family_rhymes('dog').values()))
        self.assertTrue(
            'VOCAL' in flatten(self.rd.get_family_rhymes('constantinople').values()))

    def test_partner_rhymes(self):
        self.assertTrue('HAWK' in flatten(self.rd.get_partner_rhymes('dog').values()))

    def test_additive_rhymes(self):
        self.assertTrue('DUDE' in flatten(self.rd.get_additive_rhymes('do').values()))

    def test_subtractive_rhymes(self):
        self.assertTrue('DO' in flatten(self.rd.get_subtractive_rhymes('dude').values()))
        self.assertTrue('BLUE' in flatten(self.rd.get_subtractive_rhymes('bloom').values()))
        self.assertTrue('MATTER' in flatten(self.rd.get_subtractive_rhymes('master').values()))

    def test_consonant_rhymes(self):
        self.assertTrue('BEG' in flatten(self.rd.get_consonant_rhymes('dog').values()))

    def test_assonance_rhymes(self):
        self.assertTrue('JAUNT' in flatten(self.rd.get_assonance_rhymes('dog').values()))

    def test_multisyllable_rhymes(self):
        self.assertTrue('ZOOLOGY' in flatten(self.rd.get_perfect_rhymes(
            'toxicology', num_syllables=3).values()))

    def test_substitution_rhymes(self):
        self.assertTrue('FASTER' in flatten(self.rd.get_substitution_rhymes('factor').values()))


if __name__ == '__main__':
    unittest.main()
