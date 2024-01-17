import unittest
import sys

sys.path.append("../")

from google_spreadsheets_stock_screener.Utilities.Email import Email

class TestEmail(unittest.TestCase):

    """
    Note that dummy data was used.
    """

    def test_process_single_stock_single_indicator_single_signal(self):
        email = Email(["MovingAverage"], [[["BAC", 32.12, 31.18, 31.89, 31.27, "Neutral"]]])
        self.assertDictEqual(email._process(), { "MovingAverage": { "Neutral": ["BAC"] } })

    def test_email_body_multiple_stock_multiple_indicator_single_signal(self):
        email = Email(["MovingAverage"], [[["BAC", 32.12, 31.18, 31.89, 31.27, "Neutral"]]])
        self.assertEqual(email._body, "")
    
    def test_process_multiple_stock_single_indicator_single_signal(self):
        email = Email(["MovingAverage"], [[["BAC", 32.12, 31.18, 31.89, 31.27, "Neutral"], ["TSLA", 219.91, 237.85, 212.60, 237.73, "Neutral"]]])
        self.assertDictEqual(email._process(), { "MovingAverage": { "Neutral": ["BAC", "TSLA"] } })
    
    def test_email_body_multiple_stock_multiple_indicator_single_signal(self):
        email = Email(["MovingAverage"], [[["BAC", 32.12, 31.18, 31.89, 31.27, "Neutral"], ["TSLA", 219.91, 237.85, 212.60, 237.73, "Neutral"]]])
        self.assertEqual(email._body, "")
    
    def test_process_multiple_stock_single_indicator_multiple_signal(self):
        email = Email(["MovingAverage"], [[["BAC", 32.12, 31.18, 31.89, 31.27, "Neutral"], ["TSLA", 219.91, 237.85, 212.60, 237.73, "Bullish"]]])
        self.assertDictEqual(email._process(), { "MovingAverage": { "Neutral": ["BAC"], "Bullish": ["TSLA"] } })
    
    def test_email_body_multiple_stock_multiple_indicator_single_signal(self):
        email = Email(["MovingAverage"], [[["BAC", 32.12, 31.18, 31.89, 31.27, "Neutral"], ["TSLA", 219.91, 237.85, 212.60, 237.73, "Bullish"]]])
        self.assertEqual(email._body, "MovingAverage:\nBullish:\n- TSLA")

    def test_process_single_stock_multiple_indicator_single_signal(self):
        email = Email(["MovingAverage", "RSI"], [[["BAC", 32.12, 31.18, 31.89, 31.27, "Neutral"]], [["BAC", 42.04, "Neutral"]]])
        self.assertDictEqual(email._process(), { "MovingAverage": { "Neutral": ["BAC"] }, "RSI": { "Neutral": ["BAC"] } })
    
    def test_email_body_multiple_stock_multiple_indicator_single_signal(self):
        email = Email(["MovingAverage", "RSI"], [[["BAC", 32.12, 31.18, 31.89, 31.27, "Neutral"]], [["BAC", 42.04, "Neutral"]]])
        self.assertEqual(email._body, "")
        
    def test_process_multiple_stock_multiple_indicator_single_signal(self):
        email = Email(["MovingAverage", "RSI"], [[["BAC", 32.12, 31.18, 31.89, 31.27, "Neutral"], ["AAPL", 183.63, 189.19, 181.38, 189.27, "Neutral"]], [["BAC", 42.04, "Neutral"], ["AAPL", 34.57, "Neutral"]]])
        self.assertDictEqual(email._process(), { "MovingAverage": { "Neutral": ["BAC", "AAPL"] }, "RSI": { "Neutral": ["BAC", "AAPL"] } })
    
    def test_email_body_multiple_stock_multiple_indicator_single_signal(self):
        email = Email(["MovingAverage", "RSI"], [[["BAC", 32.12, 31.18, 31.89, 31.27, "Neutral"], ["AAPL", 183.63, 189.19, 181.38, 189.27, "Neutral"]], [["BAC", 42.04, "Neutral"], ["AAPL", 34.57, "Neutral"]]])
        self.assertEqual(email._body, "")

    def test_process_multiple_stock_multiple_indicator_multiple_signal(self):
        email = Email(["MovingAverage", "RSI"], [[["BAC", 32.12, 31.18, 31.89, 31.27, "Neutral"], ["TSLA", 219.91, 237.85, 212.60, 237.73, "Bullish"]], [["BAC", 42.04, "Neutral"], ["TSLA", 29.25, "Oversold"]]])
        self.assertDictEqual(email._process(), { "MovingAverage": { "Neutral": ["BAC"], "Bullish": ["TSLA"] }, "RSI": { "Neutral": ["BAC"], "Oversold": ["TSLA"] } })

    def test_email_body_multiple_stock_multiple_indicator_multiple_signal(self):
       email = Email(["MovingAverage", "RSI"], [[["BAC", 32.12, 31.18, 31.89, 31.27, "Neutral"], ["TSLA", 219.91, 237.85, 212.60, 237.73, "Bullish"]], [["BAC", 42.04, "Neutral"], ["TSLA", 29.25, "Oversold"]]])
       self.assertEqual(email._body, "MovingAverage:\nBullish:\n- TSLA\n\nRSI:\nOversold:\n- TSLA")

if __name__ == "__main__":
    unittest.main()