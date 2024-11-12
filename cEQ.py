#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

from cubicEquation import Fraction, Exponential

import unittest


class MyTestCase(unittest.TestCase):
    def test_fraction_new_from_int(self):
        self.assertEqual(Fraction(2), 2)

    def test_fraction_new_from_float(self):
        f = Fraction(0.5)
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 2)

    def test_fraction_new_from_fraction(self):
        f1 = Fraction(2, 3)
        f2 = Fraction(f1)
        self.assertEqual(f1, f2)

    def test_exponential_new_from_int(self):
        e = Exponential(2)
        self.assertEqual(e, 2)

    def test_exponential_new_from_float(self):
        e = Exponential(0.5)
        self.assertIsInstance(e, Fraction)

        self.assertEqual(e.numerator, 1)
        self.assertEqual(e.denominator, 2)


if __name__ == '__main__':
    unittest.main()
