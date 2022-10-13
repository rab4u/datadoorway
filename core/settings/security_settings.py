from typing import Optional

from pydantic import (BaseSettings)


class SecuritySettings(BaseSettings):

    security_enable_authorization: bool = True
    # JWT BEARER Authorization settings
    security_http_bearer_auto_error: bool = True
    security_jwt_algorithms: list = ["HS256"]
    security_jwt_secret_key: str
    security_jwt_claims: list[dict] = [{"app": "data_doorway"}]

