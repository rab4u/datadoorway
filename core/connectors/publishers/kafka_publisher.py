import asyncio
from http import HTTPStatus

from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaConnectionError, RequestTimedOutError, NotEnoughReplicasError, \
    NotEnoughReplicasAfterAppendError, NodeNotReadyError, NotLeaderForPartitionError

from core.connectors.publishers.publisher_interface import PublisherInterface
from core.models.payload_model import PayloadModel
from core.models.publisher_response_model import PublisherResponseModel


class KafkaPublisher(PublisherInterface):

    def __init__(self, params: dict):
        self.producer = AIOKafkaProducer(**params)
        self.connection_status = True

    async def start(self):
        try:
            await self.producer.start()
            self.connection_status = True
        except KafkaConnectionError as e:
            await self.producer.stop()
            self.connection_status = False
            raise e

    async def stop(self):
        await self.producer.stop()

    async def send(self, publisher: str, destination: str, payload: PayloadModel, timeout: int) -> (int, str):
        try:
            if not self.connection_status:
                await self.start()

            await asyncio.wait_for(
                self.producer.send_and_wait(topic=destination, value=payload.json().encode("utf-8")),
                timeout=timeout
            )
            status, msg = HTTPStatus.OK, "success"
        except (RequestTimedOutError, NotEnoughReplicasError,
                NotEnoughReplicasAfterAppendError, NodeNotReadyError,
                NotLeaderForPartitionError, KafkaConnectionError) as e:
            status, msg = HTTPStatus.INTERNAL_SERVER_ERROR, str(e)
        except TimeoutError:
            status, msg = HTTPStatus.INTERNAL_SERVER_ERROR, "TaskTimeoutError"

        return PublisherResponseModel(
            publisher=publisher,
            status=status,
            destination=destination,
            message=msg
        )
