from pydantic import (BaseSettings)


class PublisherSettings(BaseSettings):
    publishers: list[str] = ["console", "file", "kafka", "s3", "gcs", "bigquery"]
    publisher_enable_backup = True
