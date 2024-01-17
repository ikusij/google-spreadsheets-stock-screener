from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import re

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

load_dotenv()

def label_to_number(label: str) -> int:

    """
    Helper function that converts a Google Spreadsheet 
    label into a number.
    
    @param `str label`: the label to convert into a number.
    @return `int`: the number processed from the label.
    """

    number = 0
    for char in label:
        number = number * 26 + (ord(char) - ord('A') + 1)
    return number

def number_to_label(number: int) -> str:
   
    """
    Helper function that converts a number into 
    a Google Spreadsheet label.
    
    @param `int number`: the number to convert into a label.
    @return `int`: the number processed from the label.
    """

    label = ""
    while number > 0:
        number, mod = divmod(number - 1, 26)
        label = chr(65 + mod) + label
    return label

def get_range(start_cell: str, shape: tuple[int, int]) -> str:

    """
    Helper function used to place content in
    the correct destination.
    
    @param `str start_cell`: top-left cell destination of content to be added.
    @param `tuple[int, int] shape`: shape of content to be added.
    @return `str`: destination of content in the Google Spreadsheet.
    """

    pattern = r"([A-Z]+)(\d+)"
    label_row_start, label_col_start = re.match(pattern, start_cell).groups()

    label_row_end = number_to_label(label_to_number(label_row_start) + shape[0] - 1)
    label_col_end = int(label_col_start) + shape[1] - 1

    return f"{start_cell}:{label_row_end}{label_col_end}" 

class GoogleSheet:

    def __init__(self, spreadsheet_id: str = os.getenv("SPREADSHEET_ID")):

        """
        Establish secure-connection with Google Spreadsheet.
        """

        credentials = None

        if os.path.exists("token.json"):
            credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    
        if not credentials or not credentials.valid:

            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                credentials = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(credentials.to_json())

        try:
            
            service = build("sheets", "v4", credentials=credentials)
            self._spreadsheet = service.spreadsheets()
            self._spreadsheet_id = spreadsheet_id

        except HttpError as err:

            print(err)

    def create_new_sheet(self, sheet_name: str) -> 'Sheet':

        """
        Function that establishes connection to a specific
        sheet in the Google Spreadsheet.

        @param `str sheet_name`: The name of the sheet to establish connection.
        """

        return self.Sheet(self, sheet_name)

    class Sheet:

        def __init__(self, spreadsheet: 'GoogleSheet', sheet_name: str):

            """
            @param: `GoogleSheet spreadsheet`: Google Spreadsheet.
            @param `str sheet_name`: The name of the sheet to establish connection.
            """
            
            self._spreadsheet = spreadsheet
            
            self._sheet_name = sheet_name
            
        def read(self, range: str = None) -> list[list[str]]: 

            """
            Function that reads the data of the target range.
            
            @param `str col`: Targeted range.
            @return `list[list[str]]`: range content.
            """
            
            values = self._spreadsheet._spreadsheet.values().get(
                spreadsheetId=self._spreadsheet._spreadsheet_id, 
                range=f"{self._sheet_name}!{range}" if range is not None else f"{self._sheet_name}",
            ).execute().get("values", [])

            return values

        def read_column(self, col: str) -> list[list[str]]:

            """
            Function that reads the data of the target column.
            
            @param `str col`: Targeted column.
            @return `list[list[str]]`: column content.
            """

            values = self._spreadsheet._spreadsheet.values().get(
                spreadsheetId=self._spreadsheet._spreadsheet_id, 
                range=f"{self._sheet_name}!{col}:{col}"
            ).execute().get("values", [])

            return values[1:]

        def write(self, values: list[list[str]], start_cell: str = "A2") -> None:

            """
            Function that writes content to the sheet
            
            @param `list[list[str]] values`: content to be added to the sheet.
            @param `str start_cell`: top-left cell destination of content to be added.
            """

            self._clear()

            range = get_range(start_cell, (len(values[0]), len(values)))

            self._spreadsheet._spreadsheet.values().update(
                spreadsheetId=self._spreadsheet._spreadsheet_id, 
                range=f"{self._sheet_name}!{range}",
                valueInputOption="USER_ENTERED",
                body={"values": values}
            ).execute()

        def _clear(self) -> None:

            """
            Helper function that clears the contents, but not the headers, of the sheet.
            """

            label = number_to_label(len(self.read()[0]))
            
            self._spreadsheet._spreadsheet.values().clear(
                spreadsheetId=self._spreadsheet._spreadsheet_id, 
                range=f"{self._sheet_name}!A2:{label}",
                body={}
            ).execute()
