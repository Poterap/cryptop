import datetime
from src.parsers.D2.stooq_api import download_stooq_data
import schedule
import time
from src.log.logger import My_logger
from src.config.config_reader import read_config


config = read_config()

logger = My_logger(name=config['scheduler']['logger_name'], filename=config['scheduler']['logger_path'])


def main():

    schedule.every().day.at("10:30").do(run_job)

    while True:
        schedule.run_pending()
        time.sleep(config['scheduler']['sleep_minutes'])


def run_job():
    """
    Downloads data from stooq for all tickers
    """

    for symbol_dict in config['stooq_api']['symbols']:
        for key in symbol_dict.keys():
            info = download_stooq_data(key)
            logger.info(info)

if __name__ == "__main__":
    main()