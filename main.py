from fastapi import FastAPI
from starlette.responses import FileResponse

from API.dependencies.router_dependencies import RouterDependencies
from API.routers.publish import Publish
from core.settings.settings import Settings
from core.utilities.basics import get_env_file


app = FastAPI()

env_file = get_env_file()
settings = Settings(env_file=env_file)

# Publisher router initialization
dependencies = RouterDependencies(settings=settings).get_publish_router_dependencies()
publish = Publish(settings=settings, dependencies=dependencies)
app.include_router(router=publish.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("./static/favicon.ico")
