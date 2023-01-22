import asyncio
import uuid
from asyncio import Lock
from http import HTTPStatus
from pathlib import Path
from typing import Optional

import aiofiles.os
from aiofiles.threadpool.text import AsyncTextIOWrapper

from core.connectors.publishers.publisher_interface import PublisherInterface
from core.models.payload_model import PayloadModel
from core.models.publisher_response_model import PublisherResponseModel


class FilePublisher(PublisherInterface):
    def __init__(self, params: dict):
        self.params: dict = params
        self.file_handlers: dict = {}
        self.lock = asyncio.Lock()

    async def start(self):
        """
        :return:
        """
        # TODO: Check permissions and disk size

    async def stop(self):
        for handler in self.file_handlers.values():
            handler.close()

    async def get_or_create_file_handler(self, key: str, date_partition: str,
                                         time_partition: str) -> AsyncTextIOWrapper:
        path = f"{self.params['path']}/{key}/{date_partition}/{time_partition}"

        file_handler = self.file_handlers[key] if key in self.file_handlers else None

        if file_handler and not file_handler.closed and Path(file_handler.name).is_file():
            size_kb = await aiofiles.os.path.getsize(file_handler.name) / 1000
            if size_kb >= self.params['max_size']:
                await file_handler.close()
                self.file_handlers[key] = await aiofiles.open(file=f"{path}/dd_{uuid.uuid4()}.json", mode="w")
        else:
            await aiofiles.os.makedirs(path, exist_ok=True)
            self.file_handlers[key] = await aiofiles.open(file=f"{path}/dd_{uuid.uuid4()}.json", mode="w")

        return self.file_handlers[key]

    async def worker(self, key: str, lock: Lock, payload: PayloadModel):
        async with lock:
            created_at = payload.payload_metadata.created_at
            date_partition = created_at.strftime("%Y-%m-%d")
            time_partition = created_at.strftime("%H")
            file_handler = await self.get_or_create_file_handler(key=key, date_partition=date_partition,
                                                                 time_partition=time_partition)
            await file_handler.write(payload.json() + "\n")
            await file_handler.flush()

        return HTTPStatus.OK, "success"

    async def send(self, publisher: str, destination: str, payload: PayloadModel, timeout: int):
        file_handler: Optional[AsyncTextIOWrapper] = None
        try:
            status, msg = await asyncio.wait_for(
                self.worker(key=destination, lock=self.lock, payload=payload),
                timeout=timeout
            )

        except (PermissionError, OSError, FileNotFoundError, AttributeError, TimeoutError) as e:
            status, msg = HTTPStatus.INTERNAL_SERVER_ERROR, str(e)
            try:
                await file_handler.close()
                self.file_handlers.pop(destination)
            except (AttributeError, ValueError, KeyError):
                pass
        except TimeoutError:
            status, msg = HTTPStatus.INTERNAL_SERVER_ERROR, "TaskTimeoutError"

        return PublisherResponseModel(
            publisher=publisher,
            status=status,
            destination=destination,
            message=msg
        )
