import datetime
import os
import urllib
from log.logger import My_logger
from config.config_reader import read_config
import csv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from utils.file_functions import create_folder_in_directory


config = read_config()

logger = My_logger(name=config['stooq_api']['logger_name'], filename=config['stooq_api']['logger_path'])

def get_symbols():
    return config['stooq_api']['symbols']

def download_stooq_data(symbol: str):
    # Create a folder for the data
    dir_path = create_folder_in_directory(name='stooq_data', path='../parsers/D2/data', add_date=True)

    # Generate a filename with the symbol and the current date
    date_string = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{symbol}_{date_string}.csv"
    filepath = os.path.join(dir_path, filename)

    # Generate a URL for the data
    url = f"https://stooq.pl/q/d/l/?s={symbol}&i=d"

    try:
        # Download the data from the URL
        urllib.request.urlretrieve(url, filepath)

        # Read the first line of the file
        with open(filepath) as f:
            first_line = f.readline().strip()

        # Check if the first line indicates daily limit exceeded
        if first_line == "Przekroczony dzienny limit wywolan":
            logger.warning(f"Daily limit exceeded for {symbol}.")
            raise ValueError(f"Daily limit exceeded for {symbol}.")

        # Check if the file was downloaded successfully and is not empty
        if os.path.isfile(filename) and os.path.getsize(filename) > 0:
            logger.info(f"File downloaded successfully for {symbol} and saved in /parsers/D2/stooq_data_{date_string}/{symbol}_{date_string}.csv")
            return f"File downloaded successfully for {symbol}."
        else:
            # If the file is empty or not found, log a warning and return an error message
            if os.path.isfile(filename):
                logger.warning(f"File is empty for {symbol}.")
                return f"Failed to download file for {symbol} because file is empty."
            else:
                logger.warning(f"File not found for {symbol}.")
                return f"Failed to download file for {symbol} because file not found."
    except Exception as e:
        # If an exception is raised during the download, log an error and return an error message
        logger.error(f"Error occurred while downloading file for {symbol}: {e}")
        return f"Failed to download file for {symbol}. Error: {e}"
