from pydantic import (BaseSettings)


class SchemaSettings(BaseSettings):
    schema_enable_validations: bool = False
    schema_id_format: str = r"(\w+)\/(\w+)\/(\w+)$"
    schema_internal_path: str = None
    schema_cache_size: int = 100*1024
    schema_cache_ttl: int = 0

    # TODO: Add schema registry support and apicurio registry support
    