import re
from http import HTTPStatus
from typing import Mapping

from fastapi import HTTPException

from core.settings.security_settings import SecuritySettings


class JWTValidations:

    def __init__(
            self, settings: SecuritySettings,
            token: Mapping,
            endpoint: str,
            method: str
    ):
        self.settings = settings
        self.token = token
        self.endpoint = endpoint
        self.method = method

    def validate_scope(self):
        try:
            scopes_string: str = self.token["scope"]
        except KeyError:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=f"Exception raised while decoding JWT token. Details: Missing JWT scope")

        if not re.match(self.settings.security_jwt_scope_format, scopes_string):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Exception raised while decoding JWT token. Allowed JWT scope format:"
                       f"'<endpoint>:<role> <endpoint>:<role> <endpoint>:<role> ...'. "
                       f"Example: 'publish:admin metrics:admin'"
            )

        scopes: list[str] = scopes_string.split()

        print(self.token)
        print(self.token["scope"])
        print(self.endpoint)
        print(self.method)
