from http import HTTPStatus

from core.connectors.publishers.publisher_interface import PublisherInterface
from core.models.payload_model import PayloadModel
from core.models.publisher_response_model import PublisherResponseModel


class BigQueryPublisher(PublisherInterface):

    def __init__(self, params: dict):
        pass

    async def start(self):
        pass

    async def stop(self):
        pass

    async def send(self, publisher: str, destination: str, payload: PayloadModel, timeout: int):
        return PublisherResponseModel(
            publisher=publisher,
            status=HTTPStatus.OK,
            destination=destination,
            message="success"
        )



