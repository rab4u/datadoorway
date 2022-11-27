from enum import Enum


class Paths(Enum):
    ROOT = "/"
    PUBLISH = "/publish"
    SCHEMA = "/schema"
    SCHEMATEST = "/validate"
    METRICS = "/metrics"
    ADMIN = "/admin"
    FAVICON = "/favicon.ico"
    DOCS = "/docs"
    REDOC = "/redoc"
