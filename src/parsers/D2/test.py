from config.config_reader import read_config

def symbols():
    config = read_config()
    return config['stooq_api']['symbols']
