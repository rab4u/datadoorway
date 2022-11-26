import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse, HTMLResponse
import logging

from API.dependencies.router_dependencies import RouterDependencies
from API.metadata.doc_strings import DocStrings
from API.metadata.app import App
from API.metadata.publishers import Publishers
from API.metadata.tags import Tags
from API.routers.admin import Admin
from API.routers.publish import Publish
from API.routers.schema import Schema
from core.connectors.publishers.publisher_interface import PublisherInterface
from core.settings.settings import Settings
from core.utilities.basics import get_env_file


logger = logging.getLogger("uvicorn.info")

app = FastAPI(**App.__dict__)
publisher_objs: list[PublisherInterface] = []


def initialize_routers(settings: Settings):
    # Publisher router initialization
    dependencies = RouterDependencies(settings=settings).get_auth_dependencies()
    publish = Publish(settings=settings, dependencies=dependencies)
    app.include_router(router=publish.router)

    # Admin router initialization
    dependencies = RouterDependencies(settings=settings).get_admin_router_dependencies()
    admin = Admin(settings=settings, dependencies=dependencies)
    app.include_router(router=admin.router)

    # Schema router initialization
    if settings.schema_enable_validations:
        dependencies = RouterDependencies(settings=settings).get_auth_dependencies()
        schema = Schema(settings=settings, dependencies=dependencies)
        app.include_router(router=schema.router)


async def initialize_publishers(settings: Settings):
    for publisher in settings.publisher_publishers:
        pub = Publishers.__getitem__(publisher.upper())\
            .value(params=settings.get_settings(prefix=f"publisher_{publisher}_"))
        await pub.start()
        publisher_objs.append(pub)
        logger.info(f"Initialized {pub.__class__.__name__} successfully")


@app.on_event("startup")
async def startup_event():
    # Loading settings
    env_file = get_env_file()
    settings = Settings(env_file=env_file)
    logger.info("Loaded settings successfully")

    # Initialize publishers
    await initialize_publishers(settings=settings)

    # Initialize routers
    initialize_routers(settings=settings)
    logger.info("Initialized routers successfully")


@app.on_event("shutdown")
async def shutdown_event():
    for publisher in publisher_objs:
        await publisher.stop()
        logger.info(f"Stopped {publisher.__class__.__name__} successfully")


@app.get("/", responses=DocStrings.ROOT_ENDPOINT_DOCS,
         response_class=HTMLResponse, tags=[str(Tags.ROOT.value)])
async def root():
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


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("./static/favicon.ico")


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, reload_includes=get_env_file())
