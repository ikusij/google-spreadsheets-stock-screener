from abc import ABC, abstractmethod
import pandas

class Indicator(ABC):

    """
    Indicator Inteface.
    
    Each Indicator class must have an initialization method 
    that takes in a `str ticker` and `pandas.Series history` 
    and a value method that returns a `list[str]`.
    """

    @abstractmethod
    def __init__(self, ticker: str, history: pandas.Series) -> None:

        """
        @param `str ticker`: The ticker of the stock.
        @param `pandas.Series history`: The interday history of the stock.
        """

        pass
    
    @abstractmethod
    def value(self) -> list[str]:

        """
        @return `list[str]`: row for Google Spreadsheet.
        """

        pass
