import pandas as pd

def fill_ticker_nans(ticker_df: pd.DataFrame) -> pd.DataFrame:
    return ticker_df.fillna(0)
