from Indicator.Indicator import Indicator
import pandas

class RSI(Indicator):

    def __init__(self, ticker: str, history: pandas.Series, n: int = 14, overbought: int = 70, oversold: int = 30) -> None:
        
        """
        @param `str ticker`: The ticker of the stock.
        @param `pandas.Series history`: The interday history of the stock.
        @param `int n`: the period to perform the RSI analysis.
        @param `int overbought`: the RSI level that is considered overbought.
        @param `int oversold`: the RSI level that is considered oversold.
        """

        self.ticker = ticker

        self.history = history

        self._rsi = self._n_period_rsi(n)

        self._signal = self._signal_(overbought, oversold)
    
    def _n_period_rsi(self, n: int) -> float:

        """
        Helper function the calculate the RSI of the given stock.

        @param `int n`: the period to perform the RSI analysis.
        @return `float`: the RSI.
        """

        (average_gain, average_loss) = self._average_gain_loss(n)

        rs = average_gain / average_loss

        return 100 - 100 / (1 + rs)

    def _average_gain_loss(self, n: int) -> tuple[float, float]:

        """
        Helper function to calculate the current average gain and loss.

        @param `int n`: the period to perform the RSI analysis. 
        @param `tuple[float, float]`: the current average gain and loss.
        """

        (average_gain, average_loss) = self._first_average_gain_loss(n)

        closing = self.history["Close"][n + 1:]

        for close in closing:

            diff = close - self.curr_close

            if diff >= 0:
                average_gain = (average_gain * (n - 1) + diff) / n
                average_loss = (average_loss * (n - 1)) / n
            else:
                average_gain = (average_gain * (n - 1)) / n
                average_loss = (average_loss * (n - 1) - diff) / n

            self.curr_close = close
        
        return (average_gain, average_loss)

    def _first_average_gain_loss(self, n: int) -> tuple[float, float]:

        """
        Helper function to calculate the initial average gain and loss.

        @param `int n`: the period to perform the RSI analysis. 
        @param `tuple[float, float]`: the initial average gain and loss.
        """

        (gain, loss) = (0, 0)

        self.curr_close = self.history["Close"].iloc[0]

        closing = self.history["Close"][1:n + 1]

        for close in closing:
            
            diff = close - self.curr_close
            
            if diff >= 0:
                gain += diff
            else:
                loss -= diff

            self.curr_close = close

        average_gain = gain / n
        average_loss = loss / n

        return (average_gain, average_loss)

    def _signal_(self, overbought: int, oversold: int) -> str:

        """
        Helper function that returns the signal given by the RSI analysis on the stock.

        @param `int overbought`: the RSI level that is considered overbought.
        @param `int oversold`: the RSI level that is considered oversold.
        @return `str`: signal from RSI analysis.
        """

        if self._rsi > overbought:
            return "Overbought"
        elif self._rsi < oversold:
            return "Oversold"
        else:
            return "Neutral"

    def value(self) -> list[str]:

        """
        Function that returns a row with the RSI analysis of the stock for the Google Spreadsheet.
        
        @return `list[str]`: row for Google Spreadsheet.
        """

        return [self.ticker, self._rsi, self._signal]
    