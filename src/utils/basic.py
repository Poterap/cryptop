from src.config.config_reader import read_config
from src.log.logger import My_logger


config = read_config()

python_print = print

def print(*args, **kwargs):
    if config['utils']['print']:
        python_print(*args, **kwargs)