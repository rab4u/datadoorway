import asyncio
from http import HTTPStatus
from typing import Optional, List

from fastapi import APIRouter, Request, Body, Query
from pydantic import Required

from API.dependencies.publisher_dependencies import PublisherDependencies
from API.metadata.response_metadata import ResponseMetadata
from API.metadata.paths_metadata import PathsMetadata
from API.metadata.tags_metadata import TagsMetadata
from core.connectors.publishers.publisher_interface import PublisherInterface
from core.models.payload_metadata_model import PayloadMetadataModel
from core.models.payload_model import PayloadModel
from core.models.publisher_response_model import PublisherResponseModel
from core.settings.settings import Settings


class PublishRouter:

    def __init__(self, settings: Settings, dependencies: Optional[List], publishers: dict[str, PublisherInterface]):
        """
        Constructor for publish endpoint
        :param settings: environment settings
        :param dependencies: list dependencies for the path
        :param publishers: list of publisher objects
        """
        self.settings = settings
        self.publishers = publishers

        self.router = APIRouter(tags=[str(TagsMetadata.PUBLISH.value)], dependencies=dependencies) \
            if dependencies else APIRouter(tags=[str(TagsMetadata.PUBLISH.value)])

        # Endpoint specific dependencies
        publisher_dependencies = PublisherDependencies(settings=self.settings)

        self.router.add_api_route(
            path=str(PathsMetadata.PUBLISH.value),
            endpoint=self.get_publishers,
            dependencies=publisher_dependencies.endpoint_get_dependencies(),
            methods=["GET"],
            responses=ResponseMetadata.PUBLISHER_GET_ENDPOINT_DOCS,
            description=ResponseMetadata.PUBLISHER_GET_ENDPOINT_DOCS[HTTPStatus.OK.real]["description"]
        )

        self.router.add_api_route(
            path=str(PathsMetadata.PUBLISH.value),
            endpoint=self.post_publishers,
            methods=["POST"],
            dependencies=publisher_dependencies.endpoint_post_dependencies(),
            responses=ResponseMetadata.PUBLISHER_POST_ENDPOINT_DOCS,
            description=ResponseMetadata.PUBLISHER_POST_ENDPOINT_DOCS[HTTPStatus.MULTI_STATUS.real]["description"],
            status_code=HTTPStatus.MULTI_STATUS
        )

    async def get_publishers(self) -> dict:
        return {"publishers": self.settings.publisher_publishers}

    async def post_publishers(self,
                              request: Request,
                              payload: dict = Body(example={"event": "hello"}),
                              payload_category: str = Query(
                                  default=Required,
                                  description="payload_category is like a topic, table or bucket or directory name."
                                              "Used when writing data to the destination",
                                  regex=r"^[a-zA-Z][a-zA-Z0-9_]*$"
                              )
                              ) -> list[PublisherResponseModel]:
        """
        post the data to the publishers like kafka, s3, gcs,...
        """
        payload_metadata = PayloadMetadataModel(
            publishers=request.query_params.getlist("publishers"),
            schema_id=request.query_params.get("schema_id"),
            backup_publisher=request.query_params.get("backup_publisher"),
            auth_principal=self.settings.get_sub(),
            event_category=payload_category
        )

        enriched_payload = PayloadModel(
            payload_metadata=payload_metadata,
            payload=payload
        )

        tasks = [
                self.publishers[publisher].send(
                    publisher=publisher,
                    destination=payload_metadata.event_category,
                    payload=enriched_payload,
                    timeout=self.settings.publisher_timeout
                ) for publisher in payload_metadata.publishers
        ]

        futures = await asyncio.gather(*tasks)
        responses = [fut for fut in futures]

        return responses
