from enum import Enum

from core.connectors.publishers.bigquery_publisher import BigQueryPublisher
from core.connectors.publishers.console_publisher import ConsolePublisher
from core.connectors.publishers.file_publisher_1 import FilePublisher1
from core.connectors.publishers.gcs_publisher import GCSPublisher
from core.connectors.publishers.kafka_publisher import KafkaPublisher
from core.connectors.publishers.s3_publisher import S3Publisher


class PublishersMetadata(Enum):
    KAFKA = KafkaPublisher
    S3 = S3Publisher
    CONSOLE = ConsolePublisher
    FILE = FilePublisher1
    GCS = GCSPublisher
    BIGQUERY = BigQueryPublisher
    # SNOWFLAKE = "snowflake"
    # REDSHIFT = "redshift"


