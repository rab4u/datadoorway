from http import HTTPStatus
import logging
from core.connectors.publishers.publisher_interface import PublisherInterface
from core.connectors.services.aws.aws_wrangler import AWSWrangler
from core.models.payload_model import PayloadModel


class OpenSearchPublisher(PublisherInterface, AWSWrangler):

    def __init__(self, params: dict):
        super().__init__(**params)
        self.logger = logging.getLogger("uvicorn.info")

    async def start(self):
        pass

    async def stop(self):
        pass

    async def send(self, destination: str, payload: PayloadModel) -> (int, str):
        try:
            self.logger.info(f"Saving Data to Opensearch")
            response = self.publish_to_open_search(payload_dict=payload.payload,
                                                    index_name=payload.payload_metadata.event_category)
            if response['errors']:
                self.logger.error(','.join(response['errors']))
                return HTTPStatus.BAD_REQUEST, str(f"Failed to Send the data {','.join(response['errors'])}")
            return HTTPStatus.OK, str(f"Data has been stored to ")
        except Exception as ex:
            self.logger.error(ex)
            return HTTPStatus.INTERNAL_SERVER_ERROR, str(ex)
