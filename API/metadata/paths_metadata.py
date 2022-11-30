from enum import Enum


class PathsMetadata(Enum):
    ROOT = "/"
    PUBLISH = "/publish"
    SCHEMA = "/schema"
    SCHEMATEST = "/validate"
    METRICS = "/metrics"
    ADMIN = "/admin"
    FAVICON = "/favicon.ico"
    DOCS = "/docs"
    REDOC = "/redoc"
