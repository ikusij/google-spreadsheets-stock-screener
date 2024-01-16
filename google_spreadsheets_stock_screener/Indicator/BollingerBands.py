from Indicator.Indicator import Indicator
import pandas

class BollingerBands(Indicator):
    
    def __init__(self, ticker: str, history: pandas.Series, n: int = 20, k: int = 2):

        """
        @param `str ticker`: The ticker of the stock.
        @param `pandas.Series history`: The interday history of the stock.
        @param `int n`: the moving average period to perform the Bollinger Band analysis.
        @param `int k`: the number of standard deviations that will be used for the Bollinger Band analysis.
        """
        
        self._ticker = ticker
        
        self._history = history

        self._close = self._close_()

        self._n_day_average = self._n_day_average_(n)
        self._n_day_standard_deviation = self._n_day_standard_deviation_(n)

        self._upper_band = self._n_day_average + k * self._n_day_standard_deviation
        self._lower_band = self._n_day_average - k * self._n_day_standard_deviation

        self._signal = self._signal_()

    def _close_(self) -> float:

        """
        Helper function that returns the current price of the passed ticker.

        @return `float`: the current closing price.
        """

        closing = self._history["Close"][::-1]
        return closing.iloc[0]

    def _n_day_standard_deviation_(self, n: int) -> float:

        """
        Helper function that returns the standard deviation of prices for the given period.

        @param `int n`: the moving average period to perform the Bollinger Band analysis.
        @return `float`: the standard deviation of prices for the period.
        """

        closing = self._history["Close"][::-1][:n]

        if len(closing) != n:
            return ValueError
    
        return (sum([(close - self._n_day_average) ** 2 for close in closing]) / n) ** 0.5
    
    def _n_day_average_(self, n: int) -> float:

        """
        Helper function that returns the moving average of prices for the given period.

        @param `int n`: the moving average period to perform the Bollinger Band analysis.
        @return `float`: the moving average for the period.
        """
        
        closing = self._history["Close"][::-1][:n]
        
        if len(closing) != n:
            return ValueError

        return sum(closing) / n

    def _signal_(self) -> str:

        """
        Function that returns the signal given by the Bollinger Band analysis on the stock.

        @return `str`: signal from Bollinger Band analysis.
        """

        if self._close >= self._upper_band:
            return "Overvalued"
        elif self._close <= self._lower_band:
            return "Undervalued"
        else:
            return "Neutral"
        
    def value(self) -> list[str]:

        """
        Helper function that returns a row with the Bollinger Band analysis of the stock for the Google Spreadsheet.
        
        @return `list[str]`: row for Google Spreadsheet.
        """

        return [self._ticker, self._close, self._upper_band, self._lower_band, self._signal]
    