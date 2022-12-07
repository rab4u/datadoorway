from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel
from uuid import uuid4


class PayloadMetadataModel(BaseModel):
    payload_uuid: str = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    auth_principal: Optional[str]
    publishers: list
    backup_publisher: Optional[str]
    schema_id: Optional[str]
    event_category: str
