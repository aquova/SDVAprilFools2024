import yaml

DATABASE_PATH = "private/database.db"
CONFIG_PATH = "private/config.yaml"
with open(CONFIG_PATH) as config_file:
    cfg = yaml.safe_load(config_file)

DISCORD_KEY = cfg["discord"]
SNOWBALL_LOG = cfg["channels"]["log"]
