"""Module which configures and obtains our mongo database connection."""
from mongoengine import connect
from application.config import obtain_config

APPCONFIG = obtain_config()


def get_mongo_settings() -> dict:
    """
    Function that creates a dictionary of settings to be consumed by mongo's connect function.

    Returns:
        settings_out(dict): A dictionary of our connection settings for our mongo connection.
    """

    settings_out = {
        "host": APPCONFIG["database_config"]["dbhostname"],
        "db": APPCONFIG["database_config"]["dbname"],
        "port": int(APPCONFIG["database_config"]["dbports"]),
        "username": APPCONFIG["database_config"]["dbuser"],
        "password": APPCONFIG["database_config"]["dbpassword"],
    }
    return settings_out


def get_db_connection(alias: str = None):
    """
    Function which gets the DB connection
    """

    settings = get_mongo_settings()
    if alias is not None:
        settings["alias"] = alias

    return connect(**settings)
