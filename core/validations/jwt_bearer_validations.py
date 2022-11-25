import re
from http import HTTPStatus
from typing import Mapping

from fastapi import HTTPException
from pydantic import ValidationError

from core.settings.security_settings import SecuritySettings
from core.models.jwt_model import JWTModel


class JWTBearerValidations:

    def __init__(
            self,
            settings: SecuritySettings,
            token: Mapping,
            endpoint: str,
            method: str
    ):
        self.settings = settings
        self.token = token
        self.endpoint = endpoint
        self.method = method
        self.jwt_scope_format: str = r"^((?:[a-z]+:[a-z]+)\s?)+$"

    async def validate_jwt_scopes(self):
        scopes_string: str = self.token["scopes"]
        if not re.match(self.jwt_scope_format, scopes_string):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f"Exception raised while decoding JWT token. Allowed JWT scopes format:"
                       f"'<endpoint>:<role> <endpoint>:<role> <endpoint>:<role> ...'. "
                       f"Example: 'user:read user:write'"
            )

        scopes: list[str] = scopes_string.split(" ")
        valid_scopes: set[str] = {f"{self.endpoint[1:]}:{self.method.lower()}"}.union(
            self.settings.security_method_access_rights[self.method]
        )

        matching_scopes = set(scopes).intersection(valid_scopes)

        if not matching_scopes:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f"Exception raised while decoding JWT token. Insufficient permissions"
            )

    async def validate_jwt_token(self):
        try:
            self.settings.set_jwt_model_obj(JWTModel.parse_obj(self.token))
        except ValidationError as ve:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                                detail=f"Exception raised while decoding JWT token. Details: {ve.errors()}")


