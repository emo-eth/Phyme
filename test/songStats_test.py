import unittest
import sys
sys.path.append('../')
from Phyme import songStats as ss


class SongStatsTest(unittest.TestCase):

    def test_get_count(self):
        self.assertTrue(ss.get_count_rank("i'm") == 0)
    
    def test_get_pairs(self):
        self.assertTrue(ss.get_paired_words('say').get('way') == 0)

    def test_sort_key(self):
        results = ss.sort_words('say', ['dog', 'cat', 'way', 'today'])
        self.assertEqual(results[0], 'way')
        self.assertEqual(results[1], 'today')
    
    def test_get_count_missing(self):
        self.assertIsNone(ss.get_count_rank('asdjfklajdsa'))

    def test_get_pairs_missing(self):
        self.assertGreater(ss._sort_key('aslfjalsdf', {'say': 0}), '9999')
    
    def test_strip(self):
        self.assertEqual(ss.strip_pronunciation_marker('cat(1)'), 'cat')


if __name__ == '__main__':
    unittest.main()
