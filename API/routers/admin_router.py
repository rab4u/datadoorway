from typing import Optional, List

from fastapi import APIRouter

from API.metadata.paths_metadata import PathsMetadata
from API.metadata.tags_metadata import TagsMetadata
from API.metadata.response_metadata import ResponseMetadata

from core.models.setting_model import SettingModel
from core.settings.settings import Settings
from core.validations.admin_validations import AdminValidations


class AdminRouter:
    def __init__(self, settings: Settings, dependencies: Optional[List]):
        """
        Constructor for publish endpoint
        :param settings: environment settings
        :param dependencies:
        """
        self.settings = settings

        self.router = APIRouter(
            tags=[str(TagsMetadata.ADMIN.value)],
            dependencies=dependencies,
        ) if dependencies else APIRouter(tags=[str(TagsMetadata.ADMIN.value)])

        self.router.add_api_route(
            path=str(PathsMetadata.ADMIN.value),
            endpoint=self.get_settings,
            dependencies=None,
            methods=["GET"],
            responses=ResponseMetadata.ADMIN_GET_ENDPOINT_DOCS
        )

        self.router.add_api_route(
            path=str(PathsMetadata.ADMIN.value),
            endpoint=self.update_setting,
            dependencies=None,
            methods=["PUT"],
            responses=ResponseMetadata.ADMIN_PUT_ENDPOINT_DOCS
        )

    async def get_settings(self) -> dict:
        """
        get the settings
        """
        return {"settings": self.settings}

    async def update_setting(self, setting: SettingModel) -> dict:
        """
        update the settings with given key, value. Automatically updates the env file
        """
        admin_validations = AdminValidations(settings=self.settings)
        await admin_validations.validate_setting(key=setting.key)
        await self.settings.update_setting(key=setting.key, value=setting.value)
        return {"updated_settings": {setting.key: await self.settings.get_setting(setting.key)}}
