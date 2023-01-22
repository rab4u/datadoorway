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

    async def send(self, publisher: str, destination: str, payload: PayloadModel, timeout: int) -> (int, str):
        pass




