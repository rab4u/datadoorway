import time

from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from core.settings.publisher_settings import PublisherSettings
from core.settings.schema_settings import SchemaSettings
from core.settings.security_settings import SecuritySettings
from core.security.jwt_authorization import JWTAuthorization


class CustomMiddleware:
    def __init__(self, router_settings: PublisherSettings,
                 security_settings: SecuritySettings,
                 schema_settings: SchemaSettings):
        """
        Constructor for MiddlewareBuilder
        :param router_settings: RouterSettings instance, all the settings related to routing
        :param security_settings: SecuritySettings instance, all the settings related to Security
        :param schema_settings: SchemaSettings instance, all the setting related to schema checks
        """
        self.router_settings = router_settings
        self.security_settings = security_settings
        self.schema_settings = schema_settings

        self.jwt_authorization = JWTAuthorization(settings=self.security_settings) if \
            security_settings.security_enable_authorization else None


    async def __call__(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Middleware dispatcher call this function for every request
        :param request: Incoming Request instance
        :param call_next: Actual Request endpoint
        :return: Response instance either from middleware or actual request endpoint
        """
        start_time = time.time()
        print(self.router_settings.dict())
        print(self.security_settings.dict())
        print(self.schema_settings.dict())
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        return response
