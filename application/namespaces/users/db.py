from mongoengine import connect
from application.config import obtain_config

APPCONFIG = obtain_config()

def get_mongo_url() -> str:
    '''Function that gets mongo config from file and returns
       it as a string.'''
    db_user = APPCONFIG['database_config']['DBUSER']
    db_password = APPCONFIG['database_config']['DBPASSWORD']
    db_name = APPCONFIG['database_config']['DBNAME']
    db_host = APPCONFIG['database_config']['HOSTNAME']
    db_ports = APPCONFIG['database_config']['PORTS']

    return f'mongodb://{db_user}:{db_password}@{db_host}:{db_ports}/{db_name}'

def get_mongo_settings():
    """
    Function that creates a dictionary of settings to be consumed by mongo's connect function.

    Returns:
        settings_out(dict): A dictionary of our connection settings for our mongo connection.
    """
    settings_out = {}
    settings_out["host"] = get_mongo_url()
    return settings_out

def get_db_connection(alias:str=None, mongo_client_class=None):
    """
    Function which gets the DB connection
    """

    settings = get_mongo_settings()

    if mongo_client_class is not None:
        settings["mongo_client_class"] = mongo_client_class
    if alias is not None:
        settings["alias"] = alias

    return connect(**settings)
