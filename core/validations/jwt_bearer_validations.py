import re
from http import HTTPStatus
from typing import Mapping

from fastapi import HTTPException

from core.settings.security_settings import SecuritySettings


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
        try:
            scopes_string: str = self.token["scopes"]
        except KeyError as e:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                                detail=f"Exception raised while decoding JWT token. Details: Missing JWT scopes")

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
            self.token["exp"]
        except KeyError:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                                detail=f"Exception raised while decoding JWT token. Details: Missing 'exp' in token")

        try:
            self.token["sub"]
        except KeyError:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                                detail=f"Exception raised while decoding JWT token. Details: Missing 'sub' in token")
