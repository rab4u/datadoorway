from pydantic import (BaseSettings)


class SchemaSettings(BaseSettings):
    schema_enable_validations: bool = False
    schema_registry_url: str = None
    # Schema id format : namespace.name.version
    schema_id_format: str = r"(\w+)\.(\w+)\.(\w+)$"
