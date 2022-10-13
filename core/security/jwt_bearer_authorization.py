from http import HTTPStatus
from typing import Mapping

import jwt
from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request

from core.settings.security_settings import SecuritySettings


class JWTBearerAuthorization(HTTPBearer):
    def __init__(self, settings: SecuritySettings):
        """
        Constructor for JWTAuthorization
        :param settings: security settings to configure JWT Authorization
        """
        self.settings = settings
        super(JWTBearerAuthorization, self).__init__(
            auto_error=settings.security_http_bearer_auto_error
        )

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerAuthorization, self).__call__(request)
        decoded_token = self.decode_jwt(credentials.credentials)
        print(decoded_token)
        print(self.settings.security_jwt_claims)

    def decode_jwt(self, token: str) -> Mapping:
        try:
            decoded_token = jwt.decode(jwt=token, key=self.settings.security_jwt_secret_key)
            return decoded_token
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                                detail=f"Exception raised while decoding JWT token. Details: {e}")
