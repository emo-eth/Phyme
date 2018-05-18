import unittest
import sys
sys.path.append('../')
from Phyme import Phyme
from Phyme.util import flatten


class PhymeTest(unittest.TestCase):
    rd = Phyme()

    def test_perfect_rhymes(self):
        self.assertTrue('cog' in flatten(self.rd.get_perfect_rhymes('dog').values()))
        self.assertTrue('opal' in flatten(self.rd.get_perfect_rhymes('constantinople').values()))

    def test_family_rhymes(self):
        self.assertTrue('fob' in flatten(self.rd.get_family_rhymes('dog').values()))
        self.assertTrue(
            'vocal' in flatten(self.rd.get_family_rhymes('constantinople').values()))

    def test_partner_rhymes(self):
        self.assertTrue('hawk' in flatten(self.rd.get_partner_rhymes('dog').values()))

    def test_additive_rhymes(self):
        self.assertTrue('dude' in flatten(self.rd.get_additive_rhymes('do').values()))

    def test_subtractive_rhymes(self):
        self.assertTrue('do' in flatten(self.rd.get_subtractive_rhymes('dude').values()))
        self.assertTrue('blue' in flatten(self.rd.get_subtractive_rhymes('bloom').values()))
        self.assertTrue('matter' in flatten(self.rd.get_subtractive_rhymes('master').values()))

    def test_consonant_rhymes(self):
        self.assertTrue('beg' in flatten(self.rd.get_consonant_rhymes('dog').values()))

    def test_assonance_rhymes(self):
        self.assertTrue('jaunt' in flatten(self.rd.get_assonance_rhymes('dog').values()))

    def test_multisyllable_rhymes(self):
        self.assertTrue('zoology' in flatten(self.rd.get_perfect_rhymes(
            'toxicology', num_syllables=3).values()))

    def test_substitution_rhymes(self):
        self.assertTrue('faster' in flatten(self.rd.get_substitution_rhymes('factor').values()))
    
    def test_sorted(self):
        self.assertEqual(self.rd.get_perfect_rhymes('say')[1][0], 'way')


if __name__ == '__main__':
    unittest.main()
