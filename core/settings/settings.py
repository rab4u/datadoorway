import json

import dotenv
from pydantic.types import SecretStr

from core.settings.publisher_settings import PublisherSettings
from core.settings.schema_settings import SchemaSettings
from core.settings.security_settings import SecuritySettings
from core.settings.metrics_settings import MetricsSettings
from core.utilities.basics import get_env_file


class Settings(
    PublisherSettings,
    SchemaSettings,
    SecuritySettings,
    MetricsSettings
):

    def __init__(self, env_file: str, env_file_encoding: str = "utf-8"):
        super().__init__(
            _env_file=env_file,
            _env_file_encoding=env_file_encoding
        )

    async def update_setting(self, key: str, value: str | set | list | dict | SecretStr):
        """
        updates a single setting. Automatically also updates in env file
        :param key: key of the environment variable to update
        :param value: value of the environment variable to update
        """
        key_lower = key.lower()
        current_value = await self.get_setting(key)

        if type(current_value) == set:
            setattr(self, key_lower, value)
            value = json.dumps(list(value))
        elif type(current_value) in (list, dict):
            setattr(self, key_lower, value)
            value = json.dumps(value)
        elif type(current_value) == SecretStr:
            setattr(self, key_lower, SecretStr(value))
        else:
            setattr(self, key_lower, value)

        env_file = get_env_file()
        dotenv.load_dotenv(dotenv_path=env_file)
        dotenv.set_key(dotenv_path=env_file, key_to_set=key.upper(), value_to_set=value)

    async def get_setting(self, key) -> any:
        """
        Gets the setting related to the key
        :param key: key of the environment variable
        :return:
        """
        return getattr(self, key.lower())

    def get_settings(self, prefix: str = "", remove_prefix: bool = True) -> dict:
        settings = self.dict()
        return {key.replace(prefix, ""): settings[key] for key in settings if remove_prefix and key.startswith(prefix)}



