from fastapi import Depends, FastAPI, APIRouter
from API.v1 import auth, echo


def start_application():
    app = FastAPI(title="Datadoorway API", openapi_url="/openapi.json")
    root_router = APIRouter()
    root_router.include_router(auth.router, prefix="/auth", tags=["auth"])
    root_router.include_router(router=echo.router, prefix="/echo", tags=["echo"])
    app.include_router(router=root_router, prefix="/api")
    return app


app = start_application()
