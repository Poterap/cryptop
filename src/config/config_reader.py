import yaml

def read_config():
    config_variant = "../config/test.yaml"
    with open(config_variant, 'r') as f:
        config = yaml.safe_load(f)
    return config