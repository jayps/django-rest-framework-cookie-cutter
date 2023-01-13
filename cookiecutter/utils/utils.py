import os

from cookiecutter.utils.exceptions import EnvironmentVariableNotSetException


def get_environment_variable(name: str, raise_exception: bool = True, default=None):
    """
    Method to retrieve envrionment variables.
    @param name: The name of the environment variable to retrieve
    @param raise_exception: Indicate whether or not an exception should be raised if the variable does not have a value and there's no default set.
    @param default: Default value to return if the environment variable is not set. Setting this will ensure that no exception is returned.
    """
    val = os.environ.get(name, default)

    if raise_exception and val is None:
        raise EnvironmentVariableNotSetException(
            f"{name} is a required environment variable."
        )

    return val
