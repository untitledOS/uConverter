import toml

def get_config():
    with open("config.toml", "r") as f:
        return toml.load(f)