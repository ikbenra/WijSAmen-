import unittest
from neumann.sync import plan, select, digit_remainder

class SyncTests(unittest.TestCase):
    def test_equalization(self):
        self.assertEqual(plan(11,8).periods,(11,11,11))
        self.assertEqual(plan(11,10).periods,(11,22,11))
        self.assertEqual(plan(29,8).periods,(58,58,29))
    def test_selection(self):
        self.assertEqual(select(11)[0].middle,6)
        self.assertEqual(select(29)[0].horizon,58)
    def test_remainder(self):
        self.assertEqual(digit_remainder(11,10,0),11)
        self.assertEqual(digit_remainder(11,10,1),18)
    def test_no_candidates(self):
        with self.assertRaises(ValueError): select(1,(3,))

if __name__ == '__main__': unittest.main()
