import unittest
import sys
sys.path.append('../')
from Phyme import rhymeUtils as ru


class PhoneClasses(unittest.TestCase):

    def testPhone(self):
        vowel = next(ru.VOWELS.__iter__())
        vowel_phone = ru.Phone(vowel)
        print(vowel_phone.phone, vowel)
        self.assertEqual(vowel_phone, vowel)
        self.assertTrue(vowel_phone.is_vowel)
        self.assertFalse(vowel_phone.is_consonant)
        self.assertTrue(vowel_phone.is_voiced)
        consonant = next(ru.CONSONANTS.__iter__())
        consonant_phone = ru.Phone(consonant)
        self.assertEqual(consonant_phone, consonant)
        self.assertTrue(consonant_phone.is_consonant)
        self.assertFalse(consonant_phone.is_vowel)
        self.assertEqual(consonant_phone.is_voiced, ru.is_voiced(consonant))
    
    def testMetaPhone(self):
        # "the"
        th = "TH"
        dh = "DH"
        th_phone = ru.Phone(th)
        dh_phone = ru.Phone(dh)
        meta = ru.MetaPhone(th, dh)
        self.assertEqual(meta, th)
        self.assertEqual(meta, dh)
        self.assertEqual(meta, th_phone)
        self.assertEqual(meta, dh_phone)
        self.assertTrue(meta.is_voiced)
        # "tree"
        t = "T"
        ch = "CH"
        t_phone = ru.Phone(t)
        ch_phone = ru.Phone(ch)
        meta = ru.MetaPhone(t, ch)
        self.assertEqual(meta, t)
        self.assertEqual(meta, ch)
        self.assertEqual(meta, t_phone)
        self.assertEqual(meta, ch_phone)
        self.assertFalse(meta.is_voiced)

    def testMetaVowel(self):
            # "the"
            y = "Y"
            i = "IY"
            y_phone = ru.Phone(y)
            i_phone = ru.Phone(i)
            meta = ru.MetaVowel(y, i)
            self.assertEqual(meta, y)
            self.assertEqual(meta, i)
            self.assertEqual(meta, y_phone)
            self.assertEqual(meta, i_phone)
            self.assertTrue(meta.is_voiced)
            self.assertTrue(meta.is_vowel)
            self.assertFalse(meta.is_consonant)
            # "tree"
            w = "W"
            u = "UW"
            w_phone = ru.Phone(w)
            u_phone = ru.Phone(u)
            meta = ru.MetaVowel(w, u)
            self.assertEqual(meta, w)
            self.assertEqual(meta, u)
            self.assertEqual(meta, u_phone)
            self.assertEqual(meta, w_phone)
            self.assertTrue(meta.is_voiced)
            self.assertTrue(meta.is_vowel)
            self.assertFalse(meta.is_consonant)