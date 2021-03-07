from pathlib import Path

dataPathToOHLC = Path(
    r"C:\Users\phili\Google Drive\Code_for_bothComputers\PythonStockMarketEvalTool\PythonStockScreener\01_data\01_price_data\\"
)


pathToMasterDF = Path(
    r"C:\Users\phili\Google Drive\Code_for_bothComputers\PythonStockMarketEvalTool\PythonStockScreener\01_data\01_price_data\masterDF.csv"
)


float16Cols = ["Open", "High", "Low", "Close", "Dividends", "Stock Splits"]
float32Cols = ["Volume"]
