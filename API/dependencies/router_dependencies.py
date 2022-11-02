from typing import Optional, List

from fastapi import Depends

from core.security.jwt_bearer_authorization import JWTBearerAuthorization
from core.settings.settings import Settings
from core.validations.admin_validations import AdminValidations
from core.validations.schema_validations import SchemaValidations


class RouterDependencies:
    def __init__(self, settings: Settings):
        """
        Constructor for RouterDependencies
        :param settings: environment settings
        """
        self.settings = settings

    def get_auth_dependencies(self) -> Optional[list]:
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
        auth_dependencies = self.get_auth_dependencies()
        dependencies: list = auth_dependencies if auth_dependencies else []

        admin_validations = AdminValidations(settings=self.settings)
        dependencies.append(Depends(admin_validations))

        return dependencies if len(dependencies) != 0 else None
