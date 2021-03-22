from pathlib import Path

dataPathToOHLC = Path(
    # r"C:\Users\phili\Google Drive\Code_for_bothComputers\PythonStockMarketEvalTool\PythonStockScreener\01_data\01_price_data\\"
    r"C:\Users\Philipp\Google Drive\Code_for_bothComputers\PythonStockMarketEvalTool\PythonStockScreener\01_data\01_price_data\00_price_data_raw\\"
)


pathToMasterDF = Path(
    # r"C:\Users\phili\Google Drive\Code_for_bothComputers\PythonStockMarketEvalTool\PythonStockScreener\01_data\01_price_data\masterDF.csv"
    r"C:\Users\Philipp\Google Drive\Code_for_bothComputers\PythonStockMarketEvalTool\PythonStockScreener\01_data\01_price_data\masterDF.csv"
)

dataPathToTechIndicators = Path(
    # r"C:\Users\phili\Google Drive\Code_for_bothComputers\PythonStockMarketEvalTool\PythonStockScreener\01_data\01_price_data\\"
    r"C:\Users\Philipp\Google Drive\Code_for_bothComputers\PythonStockMarketEvalTool\PythonStockScreener\01_data\01_price_data\01_price_data_w_tech_indicators\\"
)


float16Cols = ["Open", "High", "Low", "Close", "Dividends", "Stock Splits"]
float32Cols = ["Volume"]
