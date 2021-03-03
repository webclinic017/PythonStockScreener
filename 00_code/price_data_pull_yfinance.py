# Import statements
import yfinance as yf
import pandas as pd
import os
import numpy as np
from datetime import date


def gethistoricalOHLC(ticker, start_date="2000-01-01", end_date=None):
    """finds a ticker and its representative OHLC data from yahoo finance.
    Returns a pandas dataframe"""

    if ticker is None:
        print("Ticker is empty!!!")

    if end_date == "" or end_date is None:
        end_date = str(date.today())

    # TODO #1 #create a checkup if that data is already in the database

    # instantiate the yf obj
    tickerObj = yf.Ticker(ticker)

    print(date.today())
    # get historical data
    tickerHistoricalData = tickerObj.history(
        start=start_date, end=end_date, interval="1d"
    )

    return tickerHistoricalData


hist = gethistoricalOHLC("POAHY")

print(hist.columns)

print(date.today())
