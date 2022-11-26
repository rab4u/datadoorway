import asyncio

from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaConnectionError

from core.connectors.publishers.publisher_interface import PublisherInterface


class GCSPublisher(PublisherInterface):

    def __init__(self, params: dict):
        pass

    async def start(self):
        pass

    async def stop(self):
        pass

    async def send(self):
        pass



