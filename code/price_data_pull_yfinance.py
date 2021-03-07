# Import statements
import yfinance as yf
import pandas as pd
import os
import numpy as np
from datetime import date
from pathlib import Path

from global_vars import dataPathToOHLC, pathToMasterDF, float16Cols, float32Cols


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

    # get historical data
    df = tickerObj.history(start=start_date, end=end_date, interval="1d")

    df.reset_index(inplace=True)
    # cast column types
    float16TypeCast = [col for col in df.columns if col in float16Cols]
    float32TypeCast = [col for col in df.columns if col in float32Cols]
    df["Date"] = df["Date"].dt.date
    df[float16TypeCast] = df[float16TypeCast].astype("float16")
    df[float32TypeCast] = df[float32TypeCast].astype("float32")

    return df


def saveHistStockData(ticker, tickerDF):
    """saves a retrieved historical stock data from yfinance and puts it on the drive in the feather format.
    Updates the master dataframe of stored stock data and their location.

    Parameters
    ----------
    ticker : pandas.DataFrame

    return
    ------
    data_writen_flag : bool
    """

    updateFlag = False
    first_date_of_data = tickerDF.index.min()  # get first date of the data available
    last_date_of_data = tickerDF.index.max()  # get last date of the data available
    filepath = dataPathToOHLC.joinpath(
        ticker
    )  # save the filepath to the respective ticker
    masterDF = pd.read_csv(pathToMasterDF)  # open the masterDF and update the

    if ticker in masterDF.TICKER.values:
        # check if the min and max are below or above the existing entry
        if (first_date_of_data < masterDF.FIRST_DATE_OHLC) or (
            last_date_of_data > masterDF.LAST_DATE_OHLC
        ):

            # load the dataframe from disk
            diskDF = pd.read_feather(filepath)
            # merge the dataframes
            resultDF = pd.merge(tickerDF, diskDF, how="outer").drop_duplicates(
                subset="Date"
            )

            # sort the new dataframe so we are sure everything is in order
            resultDF = resultDF.sort_values(by="Date").reset_index()
            first_date_of_data = resultDF.DATE.min()
            last_date_of_data = resultDF.DATE.max()
            updateFlag = True
            data_writen_flag = False

            return data_writen_flag

    else:
        # reindex the tickerDF to be written to feather
        resultDF = tickerDF

    newEntry = pd.DataFrame(
        {
            "TICKER": [ticker],
            "FIRST_DATE_OHLC": [first_date_of_data],
            "LAST_DATE_OHLC": [last_date_of_data],
            "FILEPATH": [filepath],
        }
    )

    # dbEntry = [ticker, ffirst_date_of_data, last_date_of_data, filepath]
    # newEntry = pd.DataFrame(
    #     data=dbEntry,
    #     columns=["TICKER", "FIRST_DATE_OHLC", "LAST_DATE_OHLC", "FILEPATH"],
    # )
    if updateFlag == True:
        masterDF = masterDF.update(newEntry)
    else:
        masterDF = masterDF.append(newEntry, ignore_index=True)

    pprint(masterDF.head())
    masterDF.to_csv(pathToMasterDF, index=False)

    # save the ticker data to a feather file
    resultDF.to_feather(filepath)

    data_writen_flag = True
    return data_writen_flag


# masterDF = pd.DataFrame(columns=['TICKER', 'FIRST_DATE_OHLC', 'LAST_DATE_OHLC', 'FILEPATH'])