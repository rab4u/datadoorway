import logging

import uvicorn
from fastapi import FastAPI

from API.dependencies.router_dependencies import RouterDependencies
from API.metadata.app_metadata import AppMetadata
from API.metadata.publishers_metadata import PublishersMetadata
from API.routers.admin_router import AdminRouter
from API.routers.publish_router import PublishRouter
from API.routers.root_router import RootRouter
from API.routers.schema_router import SchemaRouter
from core.connectors.publishers.publisher_interface import PublisherInterface
from core.settings.settings import Settings
from core.utilities.basics import get_env_file

# Globals
logger = logging.getLogger("uvicorn.info")
publishers: dict[str, PublisherInterface] = {}
app = FastAPI(**AppMetadata.__dict__)


def initialize_routers(settings: Settings):
    # Auth dependencies
    auth_dependencies = RouterDependencies(settings=settings).get_auth_dependencies()

    # Publisher router initialization
    publish = PublishRouter(settings=settings, dependencies=auth_dependencies, publishers=publishers)
    app.include_router(router=publish.router)

    # Schema router initialization
    if settings.schema_enable_validations:
        schema = SchemaRouter(settings=settings, dependencies=auth_dependencies)
        app.include_router(router=schema.router)

    # Admin router initialization
    admin_dependencies = RouterDependencies(settings=settings).get_admin_router_dependencies()
    admin = AdminRouter(settings=settings, dependencies=admin_dependencies)
    app.include_router(router=admin.router)

    # Root router
    root = RootRouter(settings=settings, dependencies=None)
    app.include_router(router=root.router)


async def initialize_publishers(settings: Settings):
    for publisher in settings.publisher_publishers:
        pub = PublishersMetadata.__getitem__(publisher.upper()) \
            .value(params=settings.get_settings(prefix=f"publisher_{publisher}_"))
        try:
            publishers[publisher] = pub
            await pub.start()
            logger.info(f"Initialized {pub.__class__.__name__} successfully")
        except Exception as e:
            logger.error(f"Initialization {pub.__class__.__name__} failed")


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
    # stopping publishers
    for publisher_obj in publishers.values():
        await publisher_obj.stop()
        logger.info(f"Stopped {publisher_obj.__class__.__name__} successfully")


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, reload_includes=get_env_file())
