from typing import Optional

from pydantic import (BaseSettings)
from pydantic.types import SecretStr


class SecuritySettings(BaseSettings):

    security_enable_authorization: bool = True
    # JWT BEARER Authorization settings
    security_http_bearer_auto_error: bool = True
    security_jwt_algorithms: list = ["HS256"]
    security_jwt_secret_key: SecretStr
    security_jwt_scopes: set[str] = {
        "publish:read", "publish:write", "publish:admin",
        "subscribe:read", "subscribe:write", "subscribe:admin",
        "schema:read", "schema:write", "schema:admin",
        "metrics:read", "metrics:admin"
    }
    security_jwt_global_scopes: set[str] = {
        "dd:read", "dd:write", "dd:admin",
    }
    security_method_access_rights: dict = {
        "GET": ["read", "write", "admin"],
        "POST": ["write", "admin"],
        "PUT": ["write", "admin"],
        "DELETE": ["admin"]
    }
