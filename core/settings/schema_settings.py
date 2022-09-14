from pydantic import (BaseSettings)


class SchemaSettings(BaseSettings):
    enable_schema_checks: bool = False
    schema_registry_url: str = None
