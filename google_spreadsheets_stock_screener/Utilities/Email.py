from email.message import EmailMessage
from collections import defaultdict
from dotenv import load_dotenv
import smtplib
import os

class Email:

    def __init__(self, sheet_names: list[str], sheet_values: list[list[list[str]]]) -> None:

        """
        @param `list[str] sheet_names`: the names of the sheets in the Google Spreadsheet.
        @param `list[list[list[str]]] sheet_values`: the content of the Google Spreadsheet.
        """
        
        self._sheet_names = sheet_names
        self._sheet_values = sheet_values

        spreadsheet_data = self._process()

        self._body = self._email_body(spreadsheet_data)
    
    def _process(self) -> dict[str, dict[str, list[str]]]:

        """
        Helper function that transforms the Google Spreadsheet content
        to a dictionary. It's purpose is to facilitate the building of 
        the email body.
        """
       
        spreadsheet_data = defaultdict(dict)

        for name, rows in zip(self._sheet_names, self._sheet_values):

            sheet = defaultdict(list)
            
            for row in rows:
                
                ticker = row[0]
                signal = row[-1]

                sheet[signal].append(ticker)
            
            spreadsheet_data[name] = sheet

        return spreadsheet_data

    def _email_body(self, spreadsheet_data: dict[str, dict[str, list[str]]]) -> str:

        """
        Helper function to build email body.
        
        @param `dict[str, dict[str, list[str]]] spreadsheet_data`: dictionary used to build the email body.
        @return `str`: the email body.
        """

        body = ""
        
        for name, indicators in spreadsheet_data.items():
            
            indicator_flag = False

            indicator_body = name + ":" + "\n"
            
            for signal, tickers in indicators.items():
               
                if signal == "Neutral":
                    continue

                indicator_flag = True

                indicator_body += signal + ":" + "\n"

                for ticker in tickers:
                    
                    indicator_body += "- " + ticker + "\n"
            
            if indicator_flag:
                
                body += indicator_body + "\n"

        return body.strip()
    
    def send(self) -> None:

        """
        Function that returns sends an email if any implemented 
        indicator has a stock without a Neutral signal.
        """

        if len(self._body) == 0:
            return

        load_dotenv()

        msg = EmailMessage()
        msg["Subject"] = "Stock Scanner"
        msg["From"] = os.getenv("EMAIL")
        msg["To"] = os.getenv("RECIPIENT")
        msg.set_content(self._body)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
        server.send_message(msg)
        server.quit()
