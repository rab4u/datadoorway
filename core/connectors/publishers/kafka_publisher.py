from http import HTTPStatus

from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaConnectionError, RequestTimedOutError, NotEnoughReplicasError, \
    NotEnoughReplicasAfterAppendError, NodeNotReadyError, NotLeaderForPartitionError

from core.connectors.publishers.publisher_interface import PublisherInterface
from core.models.payload_model import PayloadModel


class KafkaPublisher(PublisherInterface):

    def __init__(self, params: dict):
        self.producer = AIOKafkaProducer(**params)

    async def start(self):
        try:
            await self.producer.start()
        except KafkaConnectionError as e:
            await self.producer.stop()
            raise e

    async def stop(self):
        await self.producer.stop()

    async def send(self, destination: str, payload: PayloadModel) -> (int, str):
        try:
            await self.producer.send_and_wait(topic=destination, value=payload.json().encode("utf-8"))
            return HTTPStatus.OK, "success"
        except (RequestTimedOutError, NotEnoughReplicasError,
                NotEnoughReplicasAfterAppendError, NodeNotReadyError,
                NotLeaderForPartitionError) as e:
            return HTTPStatus.INTERNAL_SERVER_ERROR, str(e)
