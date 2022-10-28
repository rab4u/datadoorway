from pydantic.main import BaseModel


class PayloadModel(BaseModel):
    service_name: str
    data: dict
