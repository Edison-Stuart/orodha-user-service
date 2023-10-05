"""
Contains exceptions related to the configparser and environment variables.
"""

class VariableNotPresent(Exception):
    """
    Exception for when a certain variable that is required is not in the environment
    """
    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)
