from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel
import uuid


class PayloadMetadataModel(BaseModel):
    payload_uuid: str = uuid.uuid4()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    auth_principal: str
    publishers: list
    backup_publisher: Optional[str]
    schema_id: str
    event_category: str
