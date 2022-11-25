from http import HTTPStatus
from typing import Optional, List

from fastapi import APIRouter, Request, Body, Query
from pydantic import Required

from API.dependencies.publisher_dependencies import PublisherDependencies
from API.metadata.doc_strings import DocStrings
from API.metadata.paths import Paths
from API.metadata.tags import Tags
from core.settings.settings import Settings
from core.utilities.basics import tuple_list_to_dict
from core.models.payload_metadata_model import PayloadMetadataModel
from core.models.payload_model import PayloadModel


class Publish:

    def __init__(self, settings: Settings, dependencies: Optional[List]):
        """
        Constructor for publish endpoint
        :param settings: environment settings
        :param dependencies:
        """
        self.settings = settings

        self.router = APIRouter(tags=[str(Tags.PUBLISH.value)], dependencies=dependencies) \
            if dependencies else APIRouter(tags=[str(Tags.PUBLISH.value)])

        # Endpoint specific dependencies
        publisher_dependencies = PublisherDependencies(settings=self.settings)

        self.router.add_api_route(
            path=str(Paths.PUBLISH.value),
            endpoint=self.get_publishers,
            dependencies=publisher_dependencies.endpoint_get_dependencies(),
            methods=["GET"],
            responses=DocStrings.PUBLISHER_GET_ENDPOINT_DOCS,
            description=DocStrings.PUBLISHER_GET_ENDPOINT_DOCS[HTTPStatus.OK.real]["description"]
        )

        self.router.add_api_route(
            path=str(Paths.PUBLISH.value),
            endpoint=self.post_publishers,
            methods=["POST"],
            dependencies=publisher_dependencies.endpoint_post_dependencies(),
            responses=DocStrings.PUBLISHER_POST_ENDPOINT_DOCS,
            description=DocStrings.PUBLISHER_POST_ENDPOINT_DOCS[HTTPStatus.OK.real]["description"]
        )

    async def get_publishers(self) -> dict:
        return {"publishers": self.settings.publisher_publishers}

    async def post_publishers(self,
                              request: Request,
                              payload: dict = Body(example={"event": "hello"}),
                              event_category: str = Query(
                                  default=Required,
                                  description="event_category is like a topic, table or bucket or directory name."
                                              "Used when writing data to the destination",
                                  regex=r"^[a-zA-Z][a-zA-Z0-9_]*$"
                              )
                              ) -> dict:
        """
        post the data to the publishers like kafka, s3, gcs,...
        """
        payload_metadata = PayloadMetadataModel(
            publishers=request.query_params.getlist("publishers"),
            schema_id=request.query_params.get("schema_id"),
            backup_publisher=request.query_params.get("backup_publisher"),
            auth_principal=self.settings.get_jwt_model_obj().sub,
            event_category=event_category
        )
        return {"payload": payload, "metadata": payload_metadata}
