from pydantic.main import BaseModel


class SchemaTestModel(BaseModel):
    json_schema: dict
    data: dict
