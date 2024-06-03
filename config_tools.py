import toml, os

def get_config():
    try:
        user = os.getlogin()
        with open(f"/home/{user}/.config/uconverter/config.toml", "r") as f:
            return toml.load(f)
    except FileNotFoundError:
        with open(os.path.join(os.path.dirname(__file__), "core_config.toml"), "r") as f:
            return toml.load(f)
