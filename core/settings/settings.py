import json

import dotenv

from core.settings.publisher_settings import PublisherSettings
from core.settings.schema_settings import SchemaSettings
from core.settings.security_settings import SecuritySettings
from core.utilities.basics import get_env_file


class Settings(
    PublisherSettings,
    SchemaSettings,
    SecuritySettings
):

    def __init__(self, env_file: str, env_file_encoding: str = "utf-8"):
        super().__init__(
            _env_file=env_file,
            _env_file_encoding=env_file_encoding
        )

    def update_settings(self, key: str, value: str | set | list):
        """
        updates the env file
        :param key: key of the environment variable to update
        :param value: value of the environment variable to update
        :return:
        """
        current_value = getattr(self, key.lower())

        if type(current_value) == set:
            value = json.dumps(list(value))
        elif type(current_value) == list:
            value = json.dumps(value)

        setattr(self, key.lower(), value)

        env_file = get_env_file()
        dotenv.load_dotenv(dotenv_path=env_file)
        dotenv.set_key(dotenv_path=env_file, key_to_set=key.upper(), value_to_set=value)


if __name__ == '__main__':
    s = Settings(
        env_file=get_env_file()
    )

    val = {"console", "file", "kafka", "s3", "gcs", "bigquery", "athena"}
    s.update_settings(key="publisher_publishers", value=val)
