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
        return HTTPStatus.OK, payload
