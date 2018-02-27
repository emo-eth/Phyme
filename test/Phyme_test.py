import unittest
import sys
sys.path.append('../src')
from Phyme import Phyme


class PhymeTest(unittest.TestCase):
    rd = Phyme()

    def test_perfect_rhyme(self):
        self.assertTrue('COG' in self.rd.get_perfect_rhymes('dog'))
        self.assertTrue('OPAL' in self.rd.get_perfect_rhymes('constantinople'))

    def test_family_rhyme(self):
        self.assertTrue('COB' in self.rd.get_family_rhymes('dog'))

    def test_partner_rhyme(self):
        self.assertTrue('DOCK' in self.rd.get_partner_rhymes('dog'))

    def test_additive_rhyme(self):
        self.assertTrue('DUDE' in self.rd.get_additive_rhyme('do'))

    def test_subtractive_rhyme(self):
        self.assertTrue('DO' in self.rd.get_subtractive_rhymes('dude'))

    def test_consonant_rhyme(self):
        self.assertTrue('BEG' in self.rd.get_consonant_rhyme('dog'))

    def test_assonance_rhyme(self):
        self.assertTrue('DON' in self.rd.get_assonance_rhymes('dog'))

    def test_multisyllable_rhyme(self):
        self.assertTrue('ZOOLOGY' in self.rd.get_perfect_rhymes(
            'topology', num_syllables=2))


if __name__ == '__main__':
    unittest.main()
