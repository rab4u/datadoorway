from fastapi import FastAPI
from starlette.responses import FileResponse, HTMLResponse

from API.dependencies.router_dependencies import RouterDependencies
from API.routers.admin import Admin
from API.routers.publish import Publish
from core.settings.settings import Settings
from core.utilities.basics import get_env_file

title: str = "DataDoorway (DD)"
description: str = "Simplifies data transfer in the data multiverse"
license_info: str = "Apache 2.0"

app = FastAPI(
    title=title,
    description=description,
    version="1.0",
    terms_of_service="https://github.com/rab4u/datadoorway/blob/main/CODE_OF_CONDUCT.md",
    license_info={
        "name": license_info,
        "url": "https://github.com/rab4u/datadoorway/blob/main/LICENSE",
    },
)

env_file = get_env_file()
settings = Settings(env_file=env_file)

# Publisher router initialization
dependencies = RouterDependencies(settings=settings).get_publish_router_dependencies()
publish = Publish(settings=settings, dependencies=dependencies)
app.include_router(router=publish.router)

# Admin router initialization
dependencies = RouterDependencies(settings=settings).get_admin_router_dependencies()
admin = Admin(settings=settings, dependencies=dependencies)
app.include_router(router=admin.router)


@app.get("/")
async def root():
    html_content = f"""
    <html>
    <body>
    <h1>Welcome to {title}</h1>
    <h2>{description}<h2>
    <h2>License: {license_info}<h2>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("./static/favicon.ico")
