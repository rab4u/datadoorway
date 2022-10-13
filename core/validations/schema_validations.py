from http import HTTPStatus

from fastapi import HTTPException, Query
import re

from core.settings.settings import Settings


class SchemaValidations:
    def __init__(self, settings: Settings):
        """
        Constructor for SchemaValidations
        :param settings: Setting Object
        """
        self.settings = settings

    async def __call__(self, schema_id: str = Query(
        default=None,
        description="schema id required to verify the schema of the data. Format : namespace.name.version"
    )):
        if not re.match(self.settings.schema_id_format, schema_id):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Query param is invalid. "
                       f"Allowed schema_id format : namespace.name.version. Example: sales.orders.v1"
            )
