from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from starlette.responses import HTMLResponse, FileResponse

from API.metadata.app import App
from API.metadata.doc_strings import DocStrings
from API.metadata.paths import Paths
from API.metadata.tags import Tags
from core.settings.settings import Settings


class Root:
    def __init__(self, settings: Settings, dependencies: Optional[list]):
        """
        Constructor for publish endpoint
        :param settings: environment settings
        :param dependencies:
        """
        self.settings = settings

        self.router = APIRouter(tags=[str(Tags.ROOT.value)], dependencies=dependencies) \
            if dependencies else APIRouter(tags=[str(Tags.ROOT.value)])

        self.router.add_api_route(
            path=str(Paths.ROOT.value),
            endpoint=self.get_root,
            methods=["GET"],
            responses=DocStrings.ROOT_ENDPOINT_DOCS,
            response_class=HTMLResponse
        )

        self.router.add_api_route(
            path=str(Paths.FAVICON.value),
            endpoint=self.get_favicon,
            methods=["GET"],
            include_in_schema=False
        )

    @staticmethod
    async def get_root():
        html_content = f"""
        <html>
        <body>
        <h1>Welcome to {App.title}</h1>
        <h2>{App.description}<h2>
        <h2>License: <a href='{App.license_info['url']}'>{App.license_info['name']}</a><h2>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)

    @staticmethod
    async def get_favicon():
        return FileResponse("./static/favicon.ico")
