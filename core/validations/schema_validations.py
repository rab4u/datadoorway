import json
from http import HTTPStatus
from pathlib import Path
import re

from fastapi import HTTPException, Query
from fastapi import Request
from jsonschema.validators import Draft202012Validator
from pydantic import Required

from core.settings.settings import SchemaSettings
from core.utilities.basics import file_exists
from API.metadata.paths import Paths

import jsonschema
from jsonschema import FormatChecker, Validator


class SchemaValidations:
    def __init__(self, settings: SchemaSettings):
        """
        Constructor for SchemaValidations
        :param settings: Setting Object
        """
        self.settings = settings

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
                    schema_uri: str = await self.get_schema_file(schema_id=schema_id)
                    jsonschema.validate(
                        instance=await request.json(),
                        schema={"$ref": schema_uri},
                        format_checker=FormatChecker()
                    )
                elif request.method == "POST" and request.url.path == Paths.SCHEMA.value:
                    schema = await request.json()
                    if schema:
                        Draft202012Validator.check_schema(schema=await request.json())
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
        except jsonschema.exceptions.ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Data Validation failed. reason: {e.message}"
            )
        except jsonschema.exceptions.SchemaError as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Schema Validation failed. reason: {e.message}"
            )
