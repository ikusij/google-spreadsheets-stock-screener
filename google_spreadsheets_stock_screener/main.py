from Indicator.BollingerBands import BollingerBands
from Indicator.MovingAverage import MovingAverage
from Utilities.GoogleSheet import GoogleSheet
from Utilities.Email import Email
from Indicator.RSI import RSI
import yfinance as yf

if __name__ == "__main__":

    spreadsheet = GoogleSheet()
    ticker_sheet = spreadsheet.create_new_sheet("Ticker")

    rows = ticker_sheet.read_column("A")

    indicator_classes = [MovingAverage, RSI, BollingerBands]

    sheet_values = []
    valid_tickers = []
    
    for row in rows:
        
        ticker = yf.Ticker(row[0])
        history = ticker.history(period="1y", interval="1d")
        
        if history.empty or len(history) < 50:
            continue

        valid_tickers.append([ticker.ticker.upper()])

        for index, indicator_class in enumerate(indicator_classes):

            indicator = indicator_class(ticker.ticker, history)
            indicator_value = indicator.value()

            try:
                sheet_values[index].append(indicator_value)
            except IndexError:
                sheet_values.append([indicator_value])
            
    ticker_sheet.write(valid_tickers)

    sheet_names = ["MovingAverage", "RSI", "BollingerBands"]

    for name, value in zip(sheet_names, sheet_values):
        sheet = spreadsheet.create_new_sheet(name)
        sheet.write(value)
    
    email = Email(sheet_names, sheet_values)
    email.send()
