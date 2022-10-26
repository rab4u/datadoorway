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
    try:
        env_file = os.environ['ENV_FILE']
    except KeyError as e:
        raise Exception("Environmental variable `ENV_FILE` is missing. "
                        "Please run the command : export ENV_FILE=test.env")
    return file_exists(file_path=env_file)


def tuple_list_to_dict(tuple_list: list[tuple]) -> dict:
    """
    Convert list of tuples to dict object
    :param tuple_list:
    :return: dict
    """
    data = {}
    for key, val in tuple_list:
        data.setdefault(key, []).append(val)

    return data
