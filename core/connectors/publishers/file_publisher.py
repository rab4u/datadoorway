import asyncio
import uuid
from asyncio import Task
from datetime import datetime
from http import HTTPStatus

import aiofiles.os
from aiofiles.threadpool.text import AsyncTextIOWrapper

from core.connectors.publishers.publisher_interface import PublisherInterface
from core.models.payload_model import PayloadModel


class FilePublisher(PublisherInterface):
    def __init__(self, params: dict):
        self.tasks: list[Task] = []
        self.params: dict = params
        self.file_handlers: dict = {}
        self.queue = asyncio.Queue()
        self.notifications = {}

    async def start(self):
        await aiofiles.os.makedirs(self.params['path'], exist_ok=True)
        for i in range(0, 2):
            self.tasks.append(asyncio.create_task(self.worker()))
            await asyncio.sleep(0.1)

    async def stop(self):
        await self.queue.join()
        for task in self.tasks:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
        for handler in self.file_handlers.values():
            handler.close()

    async def get_or_create_file_handler(self, key: str, date_partition: str = None,
                                         time_partition: str = None) -> AsyncTextIOWrapper:
        if key in self.file_handlers:
            return self.file_handlers[key]
        else:

            path = f"{self.params['path']}/{key}/{date_partition}/{time_partition}" \
                if date_partition and time_partition else f"{self.params['path']}/{key}"

            await aiofiles.os.makedirs(path, exist_ok=True)
            self.file_handlers[key] = await aiofiles.open(file=f"{path}/dd_{uuid.uuid4()}.json", mode="w")
            return self.file_handlers[key]

    async def rotate_file(self, key: str, created_at: datetime = None):
        now = datetime.utcnow()
        date_partition = now.strftime("%Y-%m-%d")
        time_partition = now.strftime("%H")

        file_handler = await self.get_or_create_file_handler(key=key, date_partition=date_partition,
                                                             time_partition=time_partition)

        try:
            size_kb = await aiofiles.os.path.getsize(file_handler.name) / 1000
            if size_kb >= self.params['max_size']:
                await file_handler.close()
                self.file_handlers.pop(key)

            if self.params['partition_enabled']:
                if created_at.strftime("%Y-%m-%d") != date_partition and \
                        created_at.strftime("%H") != time_partition:
                    await file_handler.close()
                    self.file_handlers.pop(key)

        except FileNotFoundError:
            await file_handler.close()
            self.file_handlers.pop(key)

        return await self.get_or_create_file_handler(key=key, date_partition=date_partition,
                                                     time_partition=time_partition)

    async def worker(self):
        while self.tasks:
            if self.queue:
                destination, payload, payload_id, event = await self.queue.get()
                try:
                    file_handler = await self.rotate_file(key=destination,
                                                          created_at=payload.payload_metadata.created_at)
                    await file_handler.write(payload.json() + "\n")
                    await file_handler.flush()
                    self.notifications[payload_id] = (HTTPStatus.OK, "success")
                except (PermissionError, OSError) as e:
                    self.notifications[payload_id] = (HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
                finally:
                    event.set()
                    self.queue.task_done()

    async def send(self, destination: str, payload: PayloadModel):
        event = asyncio.Event()
        payload_id = uuid.uuid4()

        await self.queue.put((destination, payload, payload_id, event))
        await asyncio.wait_for(event.wait(), 5)

        response = self.notifications[payload_id]
        self.notifications.pop(payload_id)

        del event

        return response
