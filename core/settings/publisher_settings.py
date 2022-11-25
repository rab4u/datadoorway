from pydantic import BaseSettings


class PublisherSettings(BaseSettings):
    # General publisher settings
    publisher_publishers: set[str] = {"console", "file", "kafka", "s3", "gcs", "bigquery"}

    # Kafka settings
    bootstrap_servers: str



