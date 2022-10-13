from typing import Optional, List

from fastapi import APIRouter, Depends, Request

from API.metadata.paths import Paths
from API.metadata.tags import Tags
from core.settings.settings import Settings
from core.utilities.basics import tuple_list_to_dict
from core.validations.publisher_validations import PublisherValidations


class Publish:

    def __init__(self, settings: Settings, dependencies: Optional[List]):
        self.settings = settings

        if dependencies:
            self.router = APIRouter(
                tags=[str(Tags.PUBLISH.value)],
                dependencies=dependencies
            )
        else:
            self.router = APIRouter(
                tags=[str(Tags.PUBLISH.value)]
            )

        self.router.add_api_route(
            path=str(Paths.PUBLISH.value),
            endpoint=self.get_publishers,
            methods=["GET"]
        )

        publisher_validations = PublisherValidations(settings=settings)
        post_publisher_dependencies = [Depends(publisher_validations)]

        self.router.add_api_route(
            path=str(Paths.PUBLISH.value),
            endpoint=self.post_publishers,
            methods=["POST"],
            dependencies=post_publisher_dependencies
        )

    async def get_publishers(self) -> dict:
        """
        gets the list publishers
        """
        return {"publishers": self.settings.publishers}

    async def post_publishers(self, request: Request) -> dict:
        """
        post the data to the publishers
        """
        return {"all_publishers": self.settings.publishers, "requested_publisher": tuple_list_to_dict(
            request.query_params.multi_items())}
