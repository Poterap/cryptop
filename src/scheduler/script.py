import datetime
import schedule
import time
from src.log.logger import My_logger
from src.config.config_reader import read_config


config = read_config()

logger = My_logger(name=config['scheduler']['logger_name'], filename=config['scheduler']['logger_path'])


def main():

    schedule.every(config['scheduler']['every_minutes']).minutes.do(run_job)

    while True:
        schedule.run_pending()


def run_job():
    current_time = datetime.datetime.now()
    result = f"Zadanie wykonane o {current_time}"
    print(result)

    logger.info(result)

if __name__ == "__main__":
    main()