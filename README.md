# google-spreadsheets-stock-screener

## Overview
This document provides an overview and usage guide for the Google Spreadsheets Stock Screener project. The project is designed to screen stocks using various financial indicators and integrates with Google Sheets for easy visualization and management. Additionally, on triggers the script will send an email to notify the user.

See the example Stock Screener User Interface at https://docs.google.com/spreadsheets/d/19N91RI1v-f2zCM-WoehWMlVWSAguaVMk-tPliY5w0rU/edit#gid=0

## Files Description

### main.py
The entry point of the stock screener application. It orchestrates the data fetching, processing, and updating of the Google Sheets interface.

### BollingerBands.py
Implements the Bollinger Bands indicator, a popular financial trading tool used to determine overbought or oversold conditions in the price of a stock.

### RSI.py
Implements the Relative Strength Index (RSI) indicator, another widely used momentum oscillator that measures the speed and change of price movements.

### MovingAverage.py
Calculates moving averages for stocks, a fundamental component in financial analysis for identifying trends.

### Indicator.py
The interface file for the Indicator class. The above files utilize this interface to properly implement the `__init__()` and `values()` functions. 

The main and Indicator files make it easy to implement new indicator classes to suit the needs of the user. The above indicators where implemented for my needs. 

### Email.py
Handles sending email notifications, possibly related to stock alerts or summary reports based on certain conditions or thresholds.

### GoogleSheet.py
Manages interactions with Google Sheets, such as updating cells, rows, or columns with the latest stock data and analysis results.

## Usage
s
In the Ticker tab of the google spreadsheet add the ticker that you want to screen. Don't worry about entering an erroneous ticker as the application will handle and eliminate them from the Ticker tab on update. 

When Implementing a new indicator class make sure to create a new Tab on the GoogleSpreadsheet with the desired name; by convention se the indicator name. Inside this tab add your desired column names, by convention the first should be Ticker and the last Signal, the rest is up to you.

In the repository create the new class in the Indicator subfolder, make sure to import Indicator and create a class which inherits from this Indicator class. For the return value in your `values()` function make sure that the array matches your indicator tab headers in the GoogleSpreadsheet. 

Finally in the main.py file import the new indicator and add the class to indicator_classes array and the spreadsheet name to the sheet_names array. 

That's it :)
