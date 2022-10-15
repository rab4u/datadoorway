from typing import Optional

from fastapi import Depends

from core.settings.settings import Settings
from core.validations.publisher_validations import PublisherValidations
from core.validations.schema_validations import SchemaValidations


class PublisherDependencies:

    def __init__(self, settings: Settings):
        """
        Constructor for MiddlewareBuilder
        :param settings: environment settings
        """
        self.settings = settings

    def endpoint_post_dependencies(self) -> Optional[list[Depends]]:
        """
        Publisher post endpoint dependencies
        :return: list[Depends]
        """
        publisher_validations = PublisherValidations(settings=self.settings)
        post_publisher_dependencies = [Depends(publisher_validations)]

        if self.settings.schema_enable_validations:
            schema_validations = SchemaValidations(settings=self.settings)
            post_publisher_dependencies.append(Depends(schema_validations))

        return post_publisher_dependencies

    def endpoint_get_dependencies(self) -> Optional[list[Depends]]:
        """
        Publisher get endpoint dependencies
        :return: None or list[Depends]
        """
        settings = self.settings
        return None
