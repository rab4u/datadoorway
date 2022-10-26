from pydantic import (BaseSettings)
from pydantic.types import SecretStr


class SecuritySettings(BaseSettings):
    security_enable_authorization: bool = True
    security_http_bearer_auto_error: bool = True
    security_jwt_algorithms: list = ["HS256"]
    security_jwt_secret_key: SecretStr
    security_admin_secret: SecretStr
    security_enable_scopes: bool = True
    security_method_access_rights: dict = {
        "GET": ["dd:read", "dd:write", "dd:admin"],
        "POST": ["dd:write", "dd:admin"],
        "PUT": ["dd:write", "dd:admin"],
        "DELETE": ["dd:admin"]
    }
