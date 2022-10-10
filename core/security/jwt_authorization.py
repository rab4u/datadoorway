from fastapi import Depends, Header, HTTPException
from fastapi_jwt_auth import AuthJWT

from core.settings.security_settings import SecuritySettings


class JWTAuthorization:
    def __init__(self, settings: SecuritySettings):
        """
        Constructor for JWTAuthorization
        :param settings: security settings to configure JWT Authorization
        """
        self.settings = settings

        @AuthJWT.load_config
        def get_config():
            """
            callback to get Security setting for AuthJWT
            """
            return self.settings


async def verify_token(x_token: str = Header()):
    if x_token != "hello":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
