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


if __name__ == '__main__':
    s = Settings(
        env_file=get_env_file()
    )
    print(s.publishers)
