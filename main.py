from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from core.middleware.custom_middleware import CustomMiddleware
from core.settings.router_settings import RouterSettings
from core.settings.schema_settings import SchemaSettings
from core.settings.security_settings import SecuritySettings
from core.utilities.basics import file_exists

app = FastAPI()
env_file = "prod.env"

security_settings = SecuritySettings(_env_file=file_exists(file_path=env_file), _env_file_encoding='utf-8')
router_settings = RouterSettings(_env_file=file_exists(file_path=env_file), _env_file_encoding='utf-8')
schema_settings = SchemaSettings(_env_file=file_exists(file_path=env_file), _env_file_encoding='utf-8')

custom_middleware = CustomMiddleware(router_settings=RouterSettings(),
                                     schema_settings=SchemaSettings(),
                                     security_settings=SecuritySettings())

app.add_middleware(BaseHTTPMiddleware, dispatch=custom_middleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("./static/favicon.ico")
