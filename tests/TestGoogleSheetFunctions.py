import unittest
import sys

sys.path.append("../")

import google_spreadsheets_stock_screener.Utilities.GoogleSheet as util

class TestGoogleSheetFunctions(unittest.TestCase):

    def test_label_to_number(self):
        self.assertEqual(util.label_to_number("A"), 1)
        self.assertEqual(util.label_to_number("B"), 2)
        self.assertEqual(util.label_to_number("Z"), 26)
        self.assertEqual(util.label_to_number("AA"), 27)
        self.assertEqual(util.label_to_number("AB"), 28)

    def test_number_to_label(self):
        self.assertEqual(util.number_to_label(1), "A")
        self.assertEqual(util.number_to_label(2), "B")
        self.assertEqual(util.number_to_label(26), "Z")
        self.assertEqual(util.number_to_label(27), "AA")
        self.assertEqual(util.number_to_label(28), "AB")

    def test_get_range_square(self):
        self.assertEqual(util.get_range("A1", (1, 1)), "A1:A1")
        self.assertEqual(util.get_range("A1", (2, 2)), "A1:B2")
        self.assertEqual(util.get_range("B2", (3, 3)), "B2:D4")

    def test_get_range_row(self):
        self.assertEqual(util.get_range("A1", (1, 5)), "A1:A5")
        self.assertEqual(util.get_range("A3", (1, 3)), "A3:A5")

    def test_get_range_col(self):
        self.assertEqual(util.get_range("A1", (5, 1)), "A1:E1")
        self.assertEqual(util.get_range("C1", (3, 1)), "C1:E1")

if __name__ == "__main__":
    unittest.main()