import datetime
from src.ds.modules.eda_auto import autoeda
from src.parsers.D2.stooq_api import download_stooq_data
import schedule
import time
from src.log.logger import My_logger
from src.config.config_reader import read_config
from src.utils.file_functions import create_folder_in_directory


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
    # get folder where the files will be saved
    folder = create_folder_in_directory(name=config['stooq_api']['creating_folder']['folder_for_saving_data_name'], path_directory=config['stooq_api']['creating_folder']['folder_for_saving_data'], add_date=config['stooq_api']['creating_folder']['folder_for_saving_data_is_with_date'])
    for symbol_dict in config['stooq_api']['symbols']:
        for key in symbol_dict.keys():
            info = download_stooq_data(key)
            logger.info(info)
    auto_eda = autoeda()
    auto_eda.make_raport_from_directory(folder)

if __name__ == "__main__":
    main()