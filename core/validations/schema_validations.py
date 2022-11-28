import json
import operator
import re
from functools import partial
from http import HTTPStatus
from pathlib import Path

import fastjsonschema
from cachetools import TTLCache, cachedmethod
from fastapi import HTTPException, Query
from fastapi import Request
from pydantic import Required

from API.metadata.paths import Paths
from core.settings.settings import SchemaSettings
from core.utilities.basics import file_exists


class SchemaValidations:
    def __init__(self, settings: SchemaSettings):
        """
        Constructor for SchemaValidations
        :param settings: Setting Object
        """
        self.settings = settings
        self.cache = TTLCache(maxsize=self.settings.schema_cache_size, ttl=self.settings.schema_cache_ttl)

    def get_cache_size(self):
        return self.settings.schema_cache_size

    def get_cache_ttl(self):
        return self.settings.schema_cache_ttl

    async def get_schema_file(self, schema_id) -> str:
        """
        Get the schema of specified schema id
        :param schema_id: schema id of the schema to retrieve
        :return: file_path
        :exception: FileNotFoundError
        """
        file_path = f"{self.settings.schema_internal_path.strip('/')}/{schema_id}.json"
        schema_file = file_exists(file_path=file_path)
        return Path(schema_file).absolute().as_uri()

    @cachedmethod(operator.attrgetter('cache'))
    def create_json_validator(self, schema_id) -> partial:
        """
        This creates a json validator using fastjsonschema library
        :param schema_id: schema_id of the json schema
        :return: a json validator of partial type
        """
        file_path = f"{self.settings.schema_internal_path.strip('/')}/{schema_id}.json"
        with open(file=file_path, mode="r") as schema_file:
            schema_json = json.loads(schema_file.read())
            validator = fastjsonschema.compile(schema_json)
        return validator

    async def __call__(self, request: Request,
                       schema_id: str = Query(
                           default=Required,
                           description="schema id required to verify the schema of "
                                       "the data. Format : root/subject/name"
                       )):
        if not re.match(self.settings.schema_id_format, schema_id):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Query param is invalid. "
                       f"Allowed schema_id format : root/subject/name. Example: users/mobile/ios.json"
            )

        try:
            if self.settings.schema_internal_path:
                if request.method == "GET" and request.url.path == Paths.SCHEMA.value:
                    await self.get_schema_file(schema_id=schema_id)
                elif request.method == "POST" and request.url.path == Paths.PUBLISH.value:
                    validate = self.create_json_validator(schema_id=schema_id)
                    validate(await request.json())
                elif request.method == "POST" and request.url.path == Paths.SCHEMA.value:
                    schema = await request.json()
                    if schema:
                        fastjsonschema.compile(definition=schema)
                    else:
                        raise HTTPException(
                            status_code=HTTPStatus.BAD_REQUEST,
                            detail="Schema Validation failed. reason: Empty schema"
                        )
        except FileNotFoundError:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Invalid schema id. reason: No schema found with the schema id : {schema_id}"
            )
        except (
                fastjsonschema.JsonSchemaException,
                fastjsonschema.JsonSchemaValueException,
                fastjsonschema.JsonSchemaDefinitionException
                ) as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Validation failed. reason: {e}"
            )
