from os.path import exists
import os


def file_exists(file_path: str) -> str:
    """
    This function validates if app environment file exists or not
    :param file_path: a valid file path including file name
    :returns file_path: if file exists
    :raises FileNotFoundError: if file doesn't exist
    """
    if not exists(file_path):
        raise FileNotFoundError(file_path)
    return file_path


def get_env_file() -> str:
    """
    get the environment file path from ENV
    :return: file_path: if file exists
    """
    env_file = os.environ['ENV_FILE']
    return file_exists(file_path=env_file)

