import dotenv
from core.utilities.basics import get_env_file

_env_file = get_env_file()


async def update_env(key: str, value: str) -> dict:
    """
    updates the env file
    """
    dotenv.load_dotenv(dotenv_path=_env_file)
    dotenv.set_key(dotenv_path=_env_file, key_to_set=key, value_to_set=value)

    return {"status": "success"}
