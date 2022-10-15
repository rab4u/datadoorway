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

    def validate_scope(self):
        try:
            scopes_string: str = self.token["scope"]
        except KeyError:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=f"Exception raised while decoding JWT token. Details: Missing JWT scope")

        if not re.match(self.jwt_scope_format, scopes_string):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f"Exception raised while decoding JWT token. Allowed JWT scope format:"
                       f"'<endpoint>:<role> <endpoint>:<role> <endpoint>:<role> ...'. "
                       f"Example: 'user:read user:write'"
            )

        scopes: list[str] = scopes_string.split(" ")
        invalid = set(scopes).issubset(
            self.settings.security_jwt_scopes.union(
                self.settings.security_jwt_global_scopes
            ))

        if not invalid:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f"Exception raised while decoding JWT token. Invalid JWT scope. "
                       f"Allowed JWT scopes: {self.settings.security_jwt_scopes}"
            )

        valid_scopes = {f"{self.endpoint[1:]}:{access}" for access in self.settings.security_method_access_rights[
            self.method]}

        matching_scopes = set(scopes).intersection(valid_scopes.union(self.settings.security_jwt_global_scopes))

        if not matching_scopes:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f"Exception raised while decoding JWT token. Insufficient permissions"
            )
