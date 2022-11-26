from typing import Optional

from pydantic import (BaseSettings)
from pydantic.types import SecretStr

from core.models.jwt_model import JWTModel


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
    _jwt_model_obj: JWTModel = None

    class Config:
        underscore_attrs_are_private = True

    def set_jwt_model_obj(self, jwt_model_obj: JWTModel):
        """
        This functions sets JWTModel object
        :param jwt_model_obj: JWTModel object
        """
        self._jwt_model_obj = jwt_model_obj

    def get_jwt_model_obj(self) -> JWTModel:
        """
        This functions returns JWTModel object
        :return: JWTModel object
        """
        return self._jwt_model_obj

    def get_sub(self) -> Optional[str]:
        """
        This function gets the JWT SUB
        :return: jwt sub or None if auth is disabled
        """
        return self.get_jwt_model_obj().sub if self.get_jwt_model_obj() else None
