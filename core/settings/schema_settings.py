from pydantic import (BaseSettings)


class SchemaSettings(BaseSettings):
    schema_enable_validations: bool = False
    # Schema id format : root\subject\name
    schema_id_format: str = r"(\w+)\/(\w+)\/(\w+)$"
    schema_internal_path: str = None

    # TODO: Add schema registry support and apicurio registry support
    