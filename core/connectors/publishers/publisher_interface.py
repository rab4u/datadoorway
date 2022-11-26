from abc import abstractmethod


class PublisherInterface:
    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    @abstractmethod
    async def send(self):
        pass
