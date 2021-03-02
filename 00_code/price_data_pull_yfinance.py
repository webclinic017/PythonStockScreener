# Import statements
import yfinance as yf
import pandas as pd

# import numpy as np
from datetime import date


def gethistoricalOHLC(ticker, saving=False, start_date="2000-01-01"):
    """finds a ticker and its representative OHLC data from yahoo finance.
    Returns a pandas dataframe"""

    if ticker is None:
        print("Ticker is empty!!!")

    # TODO #1 #create a checkup if that data is already in the database

    # instantiate the yf obj
    tickerObj = yf.Ticker(ticker)

    print(date.today())
    # get historical data
    tickerHistoricalData = tickerObj.history(
        start=start_date, end="2021-02-02", interval="1d"
    )

    return tickerHistoricalData


print(gethistoricalOHLC("MSFT"))