from http import HTTPStatus

from fastapi import HTTPException, Header
from pydantic import Required
from pydantic.types import SecretStr

from core.settings.settings import Settings


class AdminValidations:
    def __init__(self, settings: Settings):
        """
        Constructor to VerifyPublisher
        :param settings: Setting Object
        """
        self.settings = settings

    async def __call__(self,
                       x_admin_secret: SecretStr = Header(default=Required,
                                                          description="Admin secret"
                                                          )):
        """
        Validate the list of publishers
        :param x_admin_secret: Admin secret
        :exception: HTTPException
        """
        invalid = self.settings.security_admin_secret == x_admin_secret
        if not invalid:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Access denied. Invalid admin secret"
            )

    async def validate_setting(self, key):
        """
        Validates the given setting key
        :param key:
        :exception: HTTPException
        """
        try:
            key_lower = key.lower()
            getattr(self.settings, key_lower)
        except AttributeError as e:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=f"Key '{key}' not found in settings. {e}")
