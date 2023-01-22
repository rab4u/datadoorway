from abc import abstractmethod

from core.models.payload_model import PayloadModel


class PublisherInterface:
    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    @abstractmethod
    async def send(self, publisher: str, destination: str, payload: PayloadModel, timeout: int):
        pass
