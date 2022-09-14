from pydantic import (BaseSettings)


class RouterSettings(BaseSettings):
    publishers: list[str] = ["console", "file", "kafka", "s3", "aws"]
    publisher_header_name: str = 'x-publisher-id'
    middleware_routes: list[str] = ["send", "metrics", "publishers"]
