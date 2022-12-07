import json
import operator
import re
from functools import partial
from http import HTTPStatus
from pathlib import Path

import fastjsonschema
from cachetools import cachedmethod, LRUCache
from fastapi import HTTPException, Query
from fastapi import Request
from pydantic import Required

from API.metadata.paths_metadata import PathsMetadata
from core.settings.settings import SchemaSettings
from core.utilities.basics import file_exists


class SchemaValidations:
    schema_dict: dict = {}
    cache: LRUCache

    def __init__(self, settings: SchemaSettings):
        """
        Constructor for SchemaValidations
        :param settings: Setting Object
        """
        self.settings = settings
        SchemaValidations.cache = LRUCache(maxsize=self.settings.schema_cache_size)

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
    def cache_schema_validator(self, schema_id: str, validator: partial = None) -> partial:
        """
        This creates a json validator using fastjsonschema library
        :param validator: a compiled json validator object
        :param schema_id: schema_id of the json schema
        :return: a json validator of partial type
        """
        if schema_id not in self.schema_dict and not validator:
            file_path = f"{self.settings.schema_internal_path.strip('/')}/{schema_id}.json"
            with open(file=file_path, mode="r") as schema_file:
                SchemaValidations.schema_dict[schema_id] = fastjsonschema.compile(
                    definition=json.loads(schema_file.read()))
        elif validator:
            SchemaValidations.schema_dict[schema_id] = validator
        return SchemaValidations.schema_dict[schema_id]

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
                if request.method == "GET" and request.url.path == PathsMetadata.SCHEMA.value:
                    await self.get_schema_file(schema_id=schema_id)
                elif request.method == "POST" and request.url.path == PathsMetadata.PUBLISH.value:
                    validate = self.cache_schema_validator(schema_id=schema_id)
                    validate(await request.json())
                elif request.method == "POST" and request.url.path == PathsMetadata.SCHEMA.value:
                    schema = await request.json()
                    if schema:
                        self.cache_schema_validator.cache_clear(SchemaValidations)
                        self.cache_schema_validator(schema_id=schema_id,
                                                    validator=fastjsonschema.compile(definition=schema))
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
