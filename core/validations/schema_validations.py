import json
from http import HTTPStatus
from pathlib import Path
import re

from fastapi import HTTPException, Query
from fastapi import Request
from pydantic import Required

from core.settings.settings import SchemaSettings
from core.utilities.basics import file_exists

import jsonschema
from jsonschema import FormatChecker


class SchemaValidations:
    def __init__(self, settings: SchemaSettings):
        """
        Constructor for SchemaValidations
        :param settings: Setting Object
        """
        self.settings = settings

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
                       f"Allowed schema_id format : namespace.name.version. Example: users/mobile/ios.json"
            )

        try:
            if self.settings.schema_internal_path:
                file_path = f"{self.settings.schema_internal_path.strip('/')}/{schema_id}.json"
                schema_file = file_exists(file_path=file_path)

                jsonschema.validate(
                    instance=await request.json(),
                    schema={"$ref": Path(schema_file).absolute().as_uri()},
                    format_checker=FormatChecker()
                )

        except FileNotFoundError:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Invalid schema id. No schema found with the schema id : {schema_id}"
            )
        except jsonschema.exceptions.ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Data Validation failed. {e.message}"
            )
