import unittest
import sys
sys.path.append('../src')
from Phyme import Phyme


class RhymeUtilsTest(unittest.TestCase):
    rd = Phyme()

    def test_perfect_rhyme(self):
        self.assertTrue('OPAL' in self.rd.get_perfect_rhymes('Constantinople'))

    def test_family_rhyme(self):
        self.assertTrue('COB' in self.rd.get_family_rhymes('dog'))

    def test_partner_rhyme(self):
        self.assertTrue('DOCK' in self.rd.get_parter_rhymes('dog'))
    
    def get_additive_rhyme(self):
        self.assertTrue('DUDE' in self.rd.get_additive_rhyme('do'))

    def get_subtractive_rhyme(self):
        self.assertTrue('DO' in self.rd.get_subtractive_rhymes('DUDE'))

    def get_consonant_rhyme(self):
        self.assertTrue('BEG' in self.rd.get_consonant_rhyme('DOG'))

    def get_multisyllable_rhyme(self):
        self.assertTrue('ZOOLOGY' in self.rd.get_perfect_rhymes('topology', num_syllables=2))

if __name__ == '__main__':
    unittest.main()
