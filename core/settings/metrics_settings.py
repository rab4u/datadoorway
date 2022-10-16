from pydantic import BaseSettings


class MetricsSettings(BaseSettings):
    metrics_publisher_enable: bool = True
