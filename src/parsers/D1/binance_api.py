import os
import requests
import pandas as pd

from src.log.logger import My_logger
from src.config.config_reader import read_config
from src.utils.file_functions import create_folder_in_directory, create_full_file_path


config = read_config()

logger = My_logger(name=config['binance_api']['logger_name'], filename=config['binance_api']['logger_path'])

def download_binance_data(crypto: str, limit: int = config['binance_api']['default_limit'], interval: str = config['binance_api']['default_interval']):
    # Construct the file path for the CSV file to save data to
    symbol = f'{crypto.upper()}USDT'
    
    info_start_date = None

    dir_path = create_folder_in_directory(name=config['binance_api']['creating_folder']['folder_for_saving_data_name'], path_directory=config['binance_api']['creating_folder']['folder_for_saving_data'], add_date=config['binance_api']['creating_folder']['folder_for_saving_data_is_wuth_dat'])

    csv_file_path = create_full_file_path(crypto, dir_path, True, ".csv")

    if os.path.exists(csv_file_path):
        # If the file already exists, read the last timestamp to start from the next minute
        df = pd.read_csv(csv_file_path)
        start_date = pd.Timestamp(df.iloc[-1]['open_time'], tz='UTC') + pd.Timedelta(minutes=1)
    else:
        # If the file does not exist, start from the beginning of Bitcoin
        start_date = pd.Timestamp('2009-01-03', tz='UTC')

    end_date = pd.Timestamp.now(tz='UTC')
    symbol = f'{crypto.upper()}USDT'

    # while True:
    for x in range(2):
        start_time = int(start_date.timestamp() * 1000)
        end_time = int(end_date.timestamp() * 1000)

        #setings params for url
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_time,
            'endTime': end_time,
            'limit': limit
        }
        
        # Retrieve data from Binance's API
        try:
            response = requests.get(config['binance_api']['binance_api_url'], params=params)
            response.raise_for_status() # raise an error for non-200 status codes
        except requests.exceptions.RequestException as e:
            # handle connection errors
            raise Exception(f'Error connecting to Binance API: {e}')

        if response.status_code == 200:
            data = response.json()
            columns = [
                'open_time', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
                'ignored'
            ]
            # Convert the data to a pandas DataFrame
            temp_df = pd.DataFrame(data, columns=columns)
            temp_df['open_time'] = pd.to_datetime(temp_df['open_time'], unit='ms')
            temp_df['close_time'] = pd.to_datetime(temp_df['close_time'], unit='ms')
            temp_df.drop('ignored', axis=1, inplace=True)

            if not temp_df.empty:
                # Update the start_date to continue from the next minute
                start_date = temp_df['open_time'].iloc[-1] + pd.Timedelta(minutes=1)
                if info_start_date is None:
                    info_start_date = str(temp_df.iloc[0]['open_time'])
                if os.path.exists(csv_file_path):
                    # Append data to an existing CSV file
                    temp_df.to_csv(csv_file_path, mode='a', index=False, header=False)
                else:
                    # Create a new CSV file with header
                    temp_df.to_csv(csv_file_path, mode='a', index=False, header=True)
            else:
                # No more data available, exit the loop
                break

            if temp_df.shape[0] < limit:
                # If the API response contains less than the requested limit of rows of data, exit the loop since no more data is available
                break

        else:
            # If the API response status code is not 200, raise an exception with the error message
            raise Exception(f'Error: {response.json()}')

    last_date = str(temp_df.iloc[-1]['close_time'])
    info = f"Updated data for {crypto} with {interval} interval from {info_start_date} to {last_date}"
    logger.info(info)
    uti.print(info)
    return info
