import json
import os
from http import HTTPStatus
from typing import Optional, List
from pathlib import Path

from fastapi import APIRouter, Request, Body, HTTPException

from API.metadata.paths import Paths
from API.metadata.tags import Tags
from API.metadata.doc_strings import DocStrings


from core.settings.settings import Settings


class Schema:
    def __init__(self, settings: Settings, dependencies: Optional[List]):
        """
        Constructor for publish endpoint
        :param settings: environment settings
        :param dependencies:
        """
        self.settings = settings

        self.router = APIRouter(
            tags=[str(Tags.VALIDATIONS.value)],
            dependencies=dependencies,
        ) if dependencies else APIRouter(tags=[str(Tags.VALIDATIONS.value)])

        self.router.add_api_route(
            path=str(Paths.SCHEMA.value),
            endpoint=self.get_schema,
            dependencies=None,
            methods=["GET"],
            responses=DocStrings.SCHEMA_GET_ENDPOINT_DOCS
        )

        self.router.add_api_route(
            path=str(Paths.SCHEMA.value),
            endpoint=self.post_schema,
            dependencies=None,
            methods=["POST"],
            responses=DocStrings.SCHEMA_POST_ENDPOINT_DOCS
        )

    async def get_schema(self, request: Request):
        """
        get the schema based on the schema_id
        """
        schema_id = request.query_params.get("schema_id")
        with open(file=f"{self.settings.schema_internal_path.strip('/')}/{schema_id}.json") as schema_file:
            schema = json.load(schema_file)

        return schema

    async def post_schema(self, request: Request, schema: dict = Body(example={"type": "object"})):
        """
        create / overwrite the existing schema based on the schema_id
        """
        schema_id = request.query_params.get("schema_id")
        file_path = Path(f"{self.settings.schema_internal_path.strip('/')}/{schema_id}.json")
        os.makedirs(name=file_path.parent, exist_ok=True)

        try:
            with open(file=file_path.absolute(), mode="w") \
                    as schema_file:
                json.dump(fp=schema_file, obj=schema, indent=4, sort_keys=True)
        except (IOError, FileNotFoundError) as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Cannot create / overwrite existing schema. reason: {e}"
            )

        return {"detail": f"Successfully updated the schema with schema id: {schema_id}"}

