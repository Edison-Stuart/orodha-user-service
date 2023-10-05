'''Configuration file that pulls config from the environment'''
import configparser
import os
from application.config.exceptions import VariableNotPresent

def _get_environment_variables(*required_variables: str) -> dict:
    """
    Helper function which looks to the environment for certain named variables.

    Args:
        required_variables(tuple[str, ..., ...]): These are a list of positional arguments which
            are expected to be strings. These args are the target variables that we are looking for.

    Raises:
        VariableNotPresent: This is a custom exception which is called when one of the
            required_variables is not present in the environment.

    Returns:
        vars_out(dict): This is a dictionary of all of the required args. The key of each argument
            is simply the same key passed in the obtain the value from the environment.
    """
    vars_out = {}
    for var in required_variables:
        vars_out[var] = os.environ.get(var)
        if vars_out[var] is None:
            raise VariableNotPresent(message=f"Environment variable: {var} is set to None")
    return vars_out


def obtain_config() -> configparser.ConfigParser:
    '''
    Function that creates and returns a configparser object which contains
    sensitive information for our application.

    Returns:
        config(ConfigParser): A ConfigParser instance which is loaded with valuable
            information for our application.
    '''
    config = configparser.ConfigParser()
    environment_vars = _get_environment_variables(
        "keycloak_server_url",
        "keycloak_realm_name",
        "keycloak_client_id",
        "keycloak_client_secret_key",
        "DBUSER",
        "DBPASSWORD",
        "DBHOSTNAME",
        "DBPORTS"
    )

    config["keycloak_config"] = {
        "keycloak_server_url": environment_vars["keycloak_server_url"],
        "keycloak_realm_name": environment_vars["keycloak_realm_name"],
        "keycloak_client_id": environment_vars["keycloak_client_id"],
        "keycloak_client_secret_key": environment_vars["keycloak_client_secret_key"]
    }
    config["database_config"] = {
        "DBUSER": environment_vars["DBUSER"],
        "DBPASSWORD": environment_vars["DBPASSWORD"],
        "DBNAME": environment_vars["DBNAME"],
        "DBHOSTNAME": environment_vars["DBHOSTNAME"],
        "DBPORTS": environment_vars["DBPORTS"],
    }
    return config
