from typing import Callable, Dict
import pandas as pd

def fill_ticker_nans(ticker_df: Dict[str, Callable[[], pd.DataFrame]]) -> pd.DataFrame:

    merged_df = pd.DataFrame()

    for file_name, load_func in ticker_df.items():
        df = load_func()
        filled_df = df.fillna(0)
        symbol_date = file_name.split('_')
        filled_df['symbol'] = symbol_date[0]
        merged_df = pd.concat([merged_df, filled_df])

    return merged_df
