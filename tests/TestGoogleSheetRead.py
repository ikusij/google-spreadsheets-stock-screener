import unittest
import sys

sys.path.append("../")

from google_spreadsheets_stock_screener.Utilities.GoogleSheet import GoogleSheet

class TestGoogleSheetRead(unittest.TestCase):

    def setUp(self):
        spreadsheet = GoogleSheet("1tr3jej1vUwRpWhkm7AdlAT7uw_n4Oy4_KIGwoOkLPUk")
        self.sheet = spreadsheet.create_new_sheet("READ")
    
    def test_read_row(self):
        self.assertEqual(self.sheet.read("A1:A2"), [["Hello"], ["World"]])
    
    def test_read_col(self):
        self.assertEqual(self.sheet.read("A1:B1"), [["Hello", "Universe"]])
    
    def test_read_square(self):
        self.assertEqual(self.sheet.read("A1:B2"), [["Hello", "Universe"], ["World", "Hello"]])
    
    def test_read_column(self):
        self.assertEqual(self.sheet.read_column("A"), [["World"]])
        self.assertEqual(self.sheet.read_column("B"), [["Hello"]])

if __name__ == "__main__":
    unittest.main()
