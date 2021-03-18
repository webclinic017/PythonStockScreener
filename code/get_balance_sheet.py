from pyfmpcloud import settings
from pyfmpcloud import company_valuation as cv
import pandas as pd



def get_balance_sheet(api_key, ticker, period, ftype):
    """For a given ticker and time period it returns the all available balance sheets as a pandas DataFrame"""
    
    settings.set_apikey(api_key)
    df = cv.balance_sheet(ticker = ticker, period = period, ftype = ftype)
    return df