import yaml

def load_yaml_config(path):
    """load YAML config file and return Python Dict."""
    with open(path) as f:
        return yaml.load(f)

def get_config(path):
    """load YAML config file and return Python Dict with defaults."""
    return load_yaml_config(path)
