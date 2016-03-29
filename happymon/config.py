import yaml

def load_yaml_config(path):
    """load YAML config file and return Python Dict."""
    with open(path) as f:
        return yaml.load(f)

def get_config(path):
    """load YAML config file and return Python Dict with defaults."""
    config = load_yaml_config(path)
    config['threshold'] = config.get('threshold', 3)
    config['frequency'] = config.get('frequency', 60)
    config['timeout']   = config.get('timeout', 20)
    return config
