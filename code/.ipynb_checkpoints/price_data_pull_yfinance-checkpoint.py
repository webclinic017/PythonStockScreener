# Import statements
import yfinance as yf
import pandas as pd
import os
import numpy as np
from datetime import date, datetime
from pathlib import Path
import pprint
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
    first_date_of_data = tickerDF.Date.min()  # get first date of the data available
    last_date_of_data = tickerDF.Date.max()  # get last date of the data available
    filepath = dataPathToOHLC.joinpath(
        ticker
    )  # save the filepath to the respective ticker
    masterDF = pd.read_csv(pathToMasterDF)  # open the masterDF and update the

    if ticker in masterDF.TICKER.values:
        masterFirstDate = masterDF.FIRST_DATE_OHLC.loc[
            masterDF["TICKER"] == ticker
        ].iloc[0]
        masterLastDate = masterDF.FIRST_DATE_OHLC.loc[
            masterDF["TICKER"] == ticker
        ].iloc[0]

        masterFirstDate = datetime.strptime(masterFirstDate, "%Y-%m-%d").date()
        masterLastDate = datetime.strptime(masterLastDate, "%Y-%m-%d").date()
        if (first_date_of_data < masterFirstDate) or (
            last_date_of_data > masterLastDate
        ):
            # load the dataframe from disk
            diskDF = pd.read_feather(filepath)
            # merge the dataframes
            resultDF = pd.merge(tickerDF, diskDF, how="outer").drop_duplicates(
                subset="Date"
            )

            # sort the new dataframe so we are sure everything is in order
            resultDF = resultDF.sort_values(by="Date").reset_index()
            first_date_of_data = resultDF.Date.min()
            last_date_of_data = resultDF.Date.max()
            updateFlag = True

    else:
        # reindex the tickerDF to be written to feather
        resultDF = tickerDF

    newEntry = pd.DataFrame(
        {
            "TICKER": [ticker],
            "FIRST_DATE_OHLC": [first_date_of_data],
            "LAST_DATE_OHLC": [last_date_of_data],
            "FILEPATH": [filepath],
        },
        index=[0],
    )

    if updateFlag == True:
        print("before update")
        masterDF.update(masterDF[["TICKER"]].merge(newEntry, "left"))
        # masterDF.merge(newEntry, how="outer", on="TICKER")
        print("updated")
    else:
        masterDF = masterDF.append(newEntry, ignore_index=True)

    masterDF.to_csv(pathToMasterDF, index=False)

    # save the ticker data to a feather file
    resultDF.to_feather(filepath)

    data_writen_flag = True
    updateFlag = False
    return data_writen_flag


masterDF = pd.DataFrame(
    columns=["TICKER", "FIRST_DATE_OHLC", "LAST_DATE_OHLC", "FILEPATH"]
)


def loadHistDataFromDisk(
    ticker, database=None, pathToDF=pathToMasterDF, online_search=True
):
    """tries to load data from disk, if available.
    In case it does not work, it tries to pull the data from yahoo finance.
    Full docu to be written"""
    # TODO #4

    assert isinstance(
        ticker, str
    ), f"Ticker should be a string but is actually of type {type(ticker)}"

    if database is None:
        try:
            database = pd.read_csv(pathToMasterDF)
        except:
            print(
                f"could not open the database dataframe. Looking for a csv under the file location {pathToDF}"
            )

    if ticker in database["TICKER"].values:

        pathToFile = database.loc[database["TICKER"] == "AAPL", "FILEPATH"].values[0]

        tickerDF = pd.read_feather(pathToFile)
    else:
        print("Could not find the files you requested!")
        if online_search == True:
            print("Try pulling the data from yfinance!")
            try:
                tickerDF = gethistoricalOHLC(ticker)
            except:
                print("Could not load the data from yfinance!")
    tickerDF['Date'] = pd.to_datetime(tickerDF['Date'])
    return tickerDF


masterDF.to_csv(pathToMasterDF, index=False)

h_MSFT = gethistoricalOHLC("MSFT", end_date="2018-12-31")
h_AAPL_short = gethistoricalOHLC("AAPL", end_date="2015-12-31")
h_AAPL_long = gethistoricalOHLC("AAPL")

saveHistStockData("MSFT", h_MSFT)
saveHistStockData("AAPL", h_AAPL_short)
test = pd.read_csv(pathToMasterDF)
print(test.head())
saveHistStockData("AAPL", h_AAPL_long)

test = pd.read_csv(pathToMasterDF)
print(test.head())


# masterDF = pd.DataFrame(columns=['TICKER', 'FIRST_DATE_OHLC', 'LAST_DATE_OHLC', 'FILEPATH'])