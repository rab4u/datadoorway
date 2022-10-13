from typing import Optional, List

from fastapi import Depends

from core.security.jwt_bearer_authorization import JWTBearerAuthorization
from core.settings.settings import Settings
from core.validations.schema_validations import SchemaValidations


class RouterDependencies:
    def __init__(self, settings: Settings):
        """
        Constructor for MiddlewareBuilder
        :param settings: environment file to get the settings
        """
        self.settings = settings

    def get_publish_router_dependencies(self) -> Optional[list]:
        """
        Prepare list of dependencies required for publisher endpoints
        :return: Optional[List]
        """
        dependencies: list = []

        if self.settings.security_enable_authorization:
            jwt_authorization = JWTBearerAuthorization(settings=self.settings)
            dependencies.append(Depends(jwt_authorization))
        if self.settings.schema_enable_validations:
            schema_validations = SchemaValidations(settings=self.settings)
            dependencies.append(Depends(schema_validations))

        return dependencies if len(dependencies) != 0 else None

    def get_validation_router_dependencies(self) -> Optional[List]:
        """
        Prepare list of dependencies required for publisher endpoints
        :return: Optional[List]
        """
        dependencies: list = []

        if self.settings.security_enable_authorization:
            jwt_authorization = JWTBearerAuthorization(settings=self.settings)
            dependencies.append(Depends(jwt_authorization))

        return dependencies if len(dependencies) != 0 else None

    def get_admin_router_dependencies(self) -> Optional[List]:
        """
        Prepare list of dependencies required for admin endpoints
        :return: Optional[List]
        """
        dependencies: list = []

        if self.settings.security_enable_authorization:
            jwt_authorization = JWTBearerAuthorization(settings=self.settings)
            dependencies.append(Depends(jwt_authorization))

        return dependencies if len(dependencies) != 0 else None

    def get_metrics_router_dependencies(self) -> Optional[List]:
        """
        Prepare list of dependencies required for metrics endpoints
        :return: Optional[List]
        """
        # TODO : Dummy function, once metrics endpoint finalized replace the below lines
        s = self.settings.security_enable_authorization
        return [] if len([s]) != 0 else None


if __name__ == '__main__':
    env_file = "/Users/ravi/git/public/datadoorway/prod.env"
    settings1 = Settings(env_file=env_file)
    rd = RouterDependencies(settings=settings1)
    k = rd.get_publish_router_dependencies()
    print(k)
