from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from starlette.responses import HTMLResponse, FileResponse

from API.metadata.app_metadata import AppMetadata
from API.metadata.response_metadata import ResponseMetadata
from API.metadata.paths_metadata import PathsMetadata
from API.metadata.tags_metadata import TagsMetadata
from core.settings.settings import Settings


class RootRouter:
    def __init__(self, settings: Settings, dependencies: Optional[list]):
        """
        Constructor for publish endpoint
        :param settings: environment settings
        :param dependencies:
        """
        self.settings = settings

        self.router = APIRouter(tags=[str(TagsMetadata.ROOT.value)], dependencies=dependencies) \
            if dependencies else APIRouter(tags=[str(TagsMetadata.ROOT.value)])

        self.router.add_api_route(
            path=str(PathsMetadata.ROOT.value),
            endpoint=self.get_root,
            methods=["GET"],
            responses=ResponseMetadata.ROOT_ENDPOINT_DOCS,
            response_class=HTMLResponse
        )

        self.router.add_api_route(
            path=str(PathsMetadata.FAVICON.value),
            endpoint=self.get_favicon,
            methods=["GET"],
            include_in_schema=False
        )

    @staticmethod
    async def get_root():
        html_content = f"""
        <html>
        <body>
        <h1>Welcome to {AppMetadata.title}</h1>
        <h2>{AppMetadata.description}<h2>
        <h2>License: <a href='{AppMetadata.license_info['url']}'>{AppMetadata.license_info['name']}</a><h2>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)

    @staticmethod
    async def get_favicon():
        return FileResponse("./static/favicon.ico")
