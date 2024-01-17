import unittest
import sys

sys.path.append("../")

from google_spreadsheets_stock_screener.Utilities.GoogleSheet import GoogleSheet

class TestGoogleSheetWrite(unittest.TestCase):      
    
    def setUp(self):

        spreadsheet = GoogleSheet("1tr3jej1vUwRpWhkm7AdlAT7uw_n4Oy4_KIGwoOkLPUk")
        self.sheet = spreadsheet.create_new_sheet("WRITE")

    def test_write_row(self):
        
        self.sheet.write([["hello"], ["world"]])
        self.assertEqual(self.sheet.read("A2:A3"), [["hello"], ["world"]])
        self.sheet._clear()

    def test_write_col(self):
        
        self.sheet.write([["hello", "world"]])
        self.assertEqual(self.sheet.read("A2:B2"), [["hello", "world"]])
        self.sheet._clear()
    
    def test_write_square(self):
        
        self.sheet.write([["hello", "world"], ["world", "hello"]])
        self.assertEqual(self.sheet.read("A2:B3"), [["hello", "world"], ["world", "hello"]])
        self.sheet._clear()
          
    def test_clear(self):
        self.sheet.write([["hello"], ["world"]])
        self.sheet._clear()
        self.assertEqual(self.sheet.read("A2:B2"), [])

if __name__ == "__main__":
    unittest.main()