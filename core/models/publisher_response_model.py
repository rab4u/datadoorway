from typing import Optional

from pydantic.main import BaseModel


class PublisherResponseModel(BaseModel):
    publisher: str
    status: int
    destination: str
    message: Optional[str]

