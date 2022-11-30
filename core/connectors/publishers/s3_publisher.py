from http import HTTPStatus

from core.connectors.publishers.publisher_interface import PublisherInterface
from core.models.payload_model import PayloadModel


class S3Publisher(PublisherInterface):

    def __init__(self, params: dict):
        pass

    async def start(self):
        pass

    async def stop(self):
        pass

    async def send(self, destination: str, payload: PayloadModel) -> (int, str):
        return HTTPStatus.INTERNAL_SERVER_ERROR, str("failed to send data to s3")




