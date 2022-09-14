from os.path import exists


def file_exists(file_path: str) -> str:
    """
    This function validates if app environment file exists or not
    :param file_path: a valid environment file path including file name
    :returns file_path: if file exists
    :raises FileNotFoundError: if file doesn't exist
    """
    if not exists(file_path):
        raise FileNotFoundError(file_path)
    return file_path
