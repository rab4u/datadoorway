from pydantic.main import BaseModel

from core.models.payload_metadata_model import PayloadMetadataModel


class PayloadModel(BaseModel):
    event_metadata: PayloadMetadataModel
    data: dict
