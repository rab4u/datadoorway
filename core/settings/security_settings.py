from typing import Optional

from pydantic import (BaseSettings)
from pydantic.types import SecretStr


class SecuritySettings(BaseSettings):

    security_enable_authorization: bool = True
    security_admin_secret: SecretStr
    security_http_bearer_auto_error: bool = True
    security_jwt_algorithms: list = ["HS256"]
    security_jwt_secret_key: SecretStr
    # Modifying the below settings can cause application to misbehave
    security_jwt_scopes: set[str] = {
        "publish:read", "publish:write",
        "schema:read", "schema:write",
        "metrics:read"
    }
    security_jwt_admin_scopes: set[str] = {
        "dd:read", "dd:write", "dd:admin",
    }
    security_method_access_rights: dict = {
        "GET": ["read", "write"],
        "POST": ["write"],
        "PUT": ["admin"],
        "DELETE": ["admin"]
    }

