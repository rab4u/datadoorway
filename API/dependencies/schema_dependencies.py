from typing import Optional

from fastapi import Depends

from core.settings.settings import Settings
from core.validations.schema_validations import SchemaValidations


class SchemaDependencies:
    def __init__(self, settings: Settings):
        """
        Constructor for RouterDependencies
        :param settings: environment settings
        """
        self.settings = settings

    def endpoint_post_dependencies(self) -> Optional[list]:
        """
        Prepare list of dependencies required for schema post endpoint
        :return: Optional[List]
        """
        dependencies: list = []

        schema_validations = SchemaValidations(settings=self.settings)
        dependencies.append(Depends(schema_validations))

        return dependencies if len(dependencies) != 0 else None

    def endpoint_get_dependencies(self) -> Optional[list]:
        """
        Prepare list of dependencies required for schema get endpoint
        :return: Optional[List]
        """
        dependencies: list = []

        schema_validations = SchemaValidations(settings=self.settings)
        dependencies.append(Depends(schema_validations))

        return dependencies if len(dependencies) != 0 else None
