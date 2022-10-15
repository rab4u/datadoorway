from typing import Optional, List

import dotenv
from fastapi import APIRouter

from API.metadata.paths import Paths
from API.metadata.tags import Tags
from core.settings.settings import Settings


class Admin:
    def __init__(self, settings: Settings, dependencies: Optional[List]):
        """
        Constructor for publish endpoint
        :param settings: environment settings
        :param dependencies:
        """
        self.settings = settings

        self.router = APIRouter(tags=[str(Tags.ADMIN.value)], dependencies=dependencies) \
            if dependencies else APIRouter(tags=[str(Tags.ADMIN.value)])

        self.router.add_api_route(
            path=str(Paths.ADMIN.value),
            endpoint=self.get_settings,
            dependencies=None,
            methods=["GET"]
        )

    async def get_settings(self) -> dict:
        """
        get the settings
        """
        return {"settings": self.settings}
