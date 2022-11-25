from aiokafka import AIOKafkaProducer
import asyncio


class KafkaPublisher:
    def __int__(self, params: dict):
        self.producer = AIOKafkaProducer(**params)
