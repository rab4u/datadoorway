from http import HTTPStatus
import logging
from core.connectors.publishers.publisher_interface import PublisherInterface
from core.connectors.services.aws.aws_wrangler import AWSWrangler
from core.models.payload_model import PayloadModel


class S3Publisher(PublisherInterface, AWSWrangler):

    def __init__(self, params: dict):
        super().__init__(**params)
        self.logger = logging.getLogger("uvicorn.info")

    async def start(self):
        pass

    async def stop(self):
        pass

    async def send(self, destination: str, payload: PayloadModel) -> (int, str):
        try:
            self.logger.info(f"Saving Data to S3")
            response = self.save_to_s3(payload_dict=payload.payload, s3_bucket=payload.payload_metadata.event_category,
                                       s3_path=payload.payload_metadata.schema_id.split("/")[-1])
            return HTTPStatus.OK, str(f"Data has been stored to {response['paths']}")
        except Exception as ex:

            return HTTPStatus.INTERNAL_SERVER_ERROR, str(ex)
