from Indicator.Indicator import Indicator
import pandas

class MovingAverage(Indicator):

    def __init__(self, ticker: str, history: pandas.Series, n: int = 50) -> None:
        
        """
        @param `str ticker`: The ticker of the stock.
        @param `pandas.Series history`: The interday history of the stock.
        @param `int n`: the moving average period to perform the Moving Average analysis.
        """

        self.ticker = ticker
        
        self.history = history
        
        self._close = self._close_()
        self._prev_close = self._close_(1)
        
        self._day_avg = self._n_day_average(n)
        self._prev_day_avg = self._n_day_average(n, 1)

        self._signal = self._signal_()   
    
    def _close_(self, offset: int = 0) -> float:

        """
        Helper function that returns the current price of the passed ticker.

        @return `float`: the current closing price.
        """

        closing = self.history["Close"][::-1]
        
        try:

            close = closing.iloc[offset]
            return close
        
        except IndexError:

            return ValueError

    def _n_day_average(self, n: int, offset: int = 0) -> float:

        """
        Helper function that returns the moving average of prices for the given period.

        @param `int n`: the moving average period to perform the Moving Average analysis.
        @param `int offset`: the offset from the current date to calculate the moving average
        @return `float`: the moving average for the period.
        """
        
        closing = self.history["Close"][::-1][offset:n + offset]
        
        if len(closing) != n:
            return ValueError

        return sum(closing) / n

    def _signal_(self) -> str:

        """
        Helper function that returns the signal given by the Bollinger Band analysis on the stock.

        @return `str`: signal from Moving Average analysis.
        """

        if (self._prev_close < self._prev_day_avg) and (self._close > self._day_avg):
            return "Bullish"
        elif (self._prev_close > self._prev_day_avg) and (self._close < self._day_avg):
            return "Bearish"
        else:
            return "Neutral"

    def value(self) -> list[str]:

        """
        Function that returns a row with the Moving Average analysis of the stock for the Google Spreadsheet.
        
        @return `list[str]`: row for Google Spreadsheet.
        """

        return [self.ticker, self._prev_close, self._prev_day_avg, self._close, self._day_avg, self._signal]
