'''Configuration file that pulls config from the environment'''
import configparser

def obtain_config():
    '''
    Function that creates and returns a configparser object which contains
    sensitive information for our application.

    Returns:
        config(ConfigParser): A ConfigParser instance which is loaded with valuable
            information for our application.
    '''
    config = configparser.ConfigParser()
    return config
