from pydantic import BaseSettings


class PublisherSettings(BaseSettings):
    publisher_publishers: set[str] = {"console", "file", "kafka", "s3", "gcs", "bigquery"}

