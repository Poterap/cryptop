import datetime
import os
import urllib.request
from src.log.logger import My_logger
from src.config.config_reader import read_config
import csv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from src.utils.file_functions import create_folder_in_directory, create_full_file_path


config = read_config()

logger = My_logger(name=config['stooq_api']['logger_name'], filename=config['stooq_api']['logger_path'])

def get_symbols():
    return config['stooq_api']['symbols']

def download_stooq_data(symbol: str):
    # Create a folder for the data
    dir_path = create_folder_in_directory(name=config['stooq_api']['creating_folder']['folder_for_saving_data_name'], path_directory=config['stooq_api']['creating_folder']['folder_for_saving_data'], add_date=config['stooq_api']['creating_folder']['folder_for_saving_data_is_with_date'])

    # Generate a filename with the symbol and the current date
    filepath = create_full_file_path(symbol, dir_path, True, ".csv")

    # Generate a URL for the data
    url_template = config['stooq_api']['stooq_api_url']
    url = url_template.format(symbol)

    try:
        # Download the data from the URL
        urllib.request.urlretrieve(url, filename=filepath)

        # Read the first line of the file
        with open(filepath) as f:
            first_line = f.readline().strip()

        # Check if the first line indicates daily limit exceeded
        if first_line == "Przekroczony dzienny limit wywolan":
            logger.warning(f"Daily limit exceeded for {symbol}.")
            raise ValueError(f"Daily limit exceeded for {symbol}.")

        # Check if the file was downloaded successfully and is not empty
        if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
            logger.info(f"File downloaded successfully for {symbol} and saved in {filepath}")
            return f"File downloaded successfully for {symbol}."
        else:
            # If the file is empty or not found, log a warning and return an error message
            if os.path.isfile(filepath):
                logger.warning(f"File is empty for {symbol}.")
                return f"Failed to download file for {symbol} because file is empty."
            else:
                logger.warning(f"File not found for {symbol}.")
                return f"Failed to download file for {symbol} because file not found."
    except Exception as e:
        # If an exception is raised during the download, log an error and return an error message
        logger.error(f"Error occurred while downloading file for {symbol}: {e}")
        return f"Failed to download file for {symbol}. Error: {e}"
    
def download_all_stooq_data():
    info_list = []
    for symbol_dict in config['stooq_api']['symbols']:
            for key in symbol_dict.keys():
                info = download_stooq_data(key)
                info_list.append(info)
                return info_list

