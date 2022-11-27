import asyncio

from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaConnectionError, RequestTimedOutError, NotEnoughReplicasError, \
    NotEnoughReplicasAfterAppendError

from core.connectors.publishers.publisher_interface import PublisherInterface
from core.models.payload_model import PayloadModel


class KafkaPublisher(PublisherInterface):

    def __init__(self, params: dict):
        loop = asyncio.get_event_loop()
        self.producer = AIOKafkaProducer(loop=loop, **params)

    async def start(self):
        try:
            await self.producer.start()
        except KafkaConnectionError as e:
            await self.producer.stop()
            raise e

    async def stop(self):
        await self.producer.stop()

    async def send(self, destination: str, payload: PayloadModel):
        try:
            await self.producer.send_and_wait(topic=destination, value=payload.json().encode("utf-8"))
        except (RequestTimedOutError, NotEnoughReplicasError, NotEnoughReplicasAfterAppendError) as e:
            pass

        return payload




