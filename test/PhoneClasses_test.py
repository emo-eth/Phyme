import unittest
import sys
sys.path.append('../')
from Phyme import rhymeUtils as ru
from Phyme.rhymeUtils import RhymeUtils


class PhoneClasses(unittest.TestCase):

    def testPhone(self):
        vowel = next(RhymeUtils.VOWELS.__iter__())
        vowel_phone = ru.Phone(vowel)
        print(vowel_phone.phone, vowel)
        self.assertEqual(vowel_phone, vowel)
        self.assertTrue(vowel_phone.is_vowel)
        self.assertFalse(vowel_phone.is_consonant)
        self.assertTrue(vowel_phone.is_voiced)
        consonant = next(RhymeUtils.CONSONANTS.__iter__())
        consonant_phone = ru.Phone(consonant)
        self.assertEqual(consonant_phone, consonant)
        self.assertTrue(consonant_phone.is_consonant)
        self.assertFalse(consonant_phone.is_vowel)
        self.assertEqual(consonant_phone.is_voiced, RhymeUtils._is_voiced(consonant))
    
    def testMetaPhone(self):
        # "the"
        th = "TH"
        dh = "DH"
        th_phone = ru.Phone(th)
        dh_phone = ru.Phone(dh)
        meta = ru.MetaPhone(th_phone, dh_phone)
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
        meta = ru.MetaPhone(t_phone, ch_phone)
        self.assertEqual(meta, t)
        self.assertEqual(meta, ch)
        self.assertEqual(meta, t_phone)
        self.assertEqual(meta, ch_phone)
        self.assertFalse(meta.is_voiced)

    def testMetaVowel(self):
            # y is i
            y = "Y"
            i = "IY"
            y_phone = ru.Phone(y)
            i_phone = ru.Phone(i)
            meta = ru.MetaVowel(y_phone, i_phone)
            meta_copy = ru.MetaVowel(y_phone, i_phone)
            self.assertEqual(meta_copy, meta)
            self.assertEqual(meta, y)
            self.assertEqual(meta, i)
            self.assertEqual(meta, y_phone)
            self.assertEqual(meta, i_phone)
            self.assertTrue(meta.is_voiced)
            self.assertTrue(meta.is_vowel)
            self.assertFalse(meta.is_consonant)
            # w is u
            w = "W"
            u = "UW"
            w_phone = ru.Phone(w)
            u_phone = ru.Phone(u)
            meta = ru.MetaVowel(w_phone, u_phone)
            self.assertEqual(meta, w)
            self.assertEqual(meta, u)
            self.assertEqual(meta, u_phone)
            self.assertEqual(meta, w_phone)
            self.assertTrue(meta.is_voiced)
            self.assertTrue(meta.is_vowel)
            self.assertFalse(meta.is_consonant)
        
    def testHash(self):
        phone1 = ru.Phone("IY")
        phone2 = ru.Phone("UW")
        phone1_copy = ru.Phone("IY")
        phone2_copy = ru.Phone("UW")
        phone_set = {phone1, phone2}
        self.assertTrue(phone1_copy in phone_set)
        self.assertTrue(phone2_copy in phone_set)

        metaPhone = ru.MetaPhone(ru.Phone("TH"), ru.Phone("DH"))
        phone3 = ru.Phone("TH")
        phone_set2 = {phone3}
        self.assertTrue(metaPhone in phone_set2)

