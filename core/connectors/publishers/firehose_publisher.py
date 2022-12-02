import json
import logging
import time
from http import HTTPStatus

from boto3.session import Session

from core.connectors.publishers.publisher_interface import PublisherInterface
from core.models.payload_model import PayloadModel


# from Fire


class FirehosePublisher(PublisherInterface):

    def __init__(self, params: dict):
        self._retry_count = 0
        self._method_response = HTTPStatus.SEE_OTHER, str(None)
        self.logger = logging.getLogger("uvicorn.info")
        self._aws_region = params["aws_region"]
        self._firehose_client = Session(region_name=self._aws_region).client("firehose")
        self._max_retries = params.get("max_retries", 3)

    async def start(self):
        pass

    async def stop(self):
        pass

    async def send(self, destination: str, payload: PayloadModel) -> (int, str):

        self._retry_count = 0
        while True:
            try:
                self.logger.info(f"Publishing to Firehose")
                response = self._firehose_client.put_record_batch(
                    Records=[
                        {
                            'Data': bytes(json.dumps(payload.payload), encoding='UTF-8')
                        },
                    ],
                    DeliveryStreamName=payload.payload_metadata.event_category
                )
                if response['FailedPutCount'] > 0:
                    self._method_response = HTTPStatus.INTERNAL_SERVER_ERROR, set([requestresponse['ErrorMessage'] for
                                                                                   requestresponse in
                                                                                   response['RequestResponses']])
                    break
                else:
                    self._method_response = HTTPStatus.OK, str(f"Data has been published to Firehose")
                    break
            except self._firehose_client.exceptions.ServiceUnavailableException as sue:
                if self._retry_count >= self._max_retries:
                    self._method_response = HTTPStatus.TOO_MANY_REQUESTS, str(sue)
                    break
                self._retry_count += 1
                time.sleep(10)
            except self._firehose_client.exceptions.ResourceNotFoundException as rnfe:
                self._method_response = HTTPStatus.NOT_FOUND, str(rnfe)
                break
            except self._firehose_client.exceptions.InvalidArgumentException | \
                   self._firehose_client.exceptions.InvalidKMSResourceException | Exception as ex:
                print(ex)
                self._method_response = HTTPStatus.BAD_REQUEST, str(ex)
                break

        return self._method_response
