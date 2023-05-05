import datetime
import os
import urllib
from log.logger import My_logger
from config.config_reader import read_config
import csv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


config = read_config()

logger = My_logger(name=config['stooq_api']['logger_name'], filename=config['stooq_api']['logger_path'])

def get_symbols():
    return config['stooq_api']['symbols']


def download_stooq_data(symbol: str):
    date_string = datetime.datetime.now().strftime("%Y-%m-%d")
    dir_name = f"../parsers/D2/data/stooq_data_{date_string}"
    os.makedirs(dir_name, exist_ok=True)
    filename = f"../parsers/D2/data/stooq_data_{date_string}/{symbol}_{date_string}.csv"
    url = f"https://stooq.pl/q/d/l/?s={symbol}&i=d"

    try:
        urllib.request.urlretrieve(url, filename)
        if os.path.isfile(filename) and os.path.getsize(filename) > 0:
            logger.info(f"File downloaded successfully for {symbol} and saved in /parsers/D2/stooq_data_{date_string}/{symbol}_{date_string}.csv")
            return f"File downloaded successfully for {symbol}."
        else:
            if os.path.isfile(filename):
                logger.warning(f"File is empty for {symbol}.")
                return f"Failed to download file for {symbol} because file is empty."
            else:
                logger.warning(f"File not found for {symbol}.")
                return f"Failed to download file for {symbol} because file not found."
    except Exception as e:
        logger.error(f"Error occurred while downloading file for {symbol}: {e}")
        return f"Failed to download file for {symbol}. Error: {e}"

