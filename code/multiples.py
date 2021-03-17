import requests
import alpha_vantage
import pandas as pd

def get_muliples(symbol, api_key):
    """finds a ticker and its representative company overview data from alphavanatge. Returns a pandas dataframe"""

    API_URL = "https://www.alphavantage.co/query"

    data = {"function": "OVERVIEW", "symbol": symbol, "apikey": api_key}
    response = requests.get(API_URL, data)
    response_json = response.json()
    
    return pd.Series(response_json)
    