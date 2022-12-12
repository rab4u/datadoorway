from enum import Enum

from core.connectors.publishers.bigquery_publisher import BigQueryPublisher
from core.connectors.publishers.console_publisher import ConsolePublisher
from core.connectors.publishers.file_publisher import FilePublisher
from core.connectors.publishers.gcs_publisher import GCSPublisher
from core.connectors.publishers.kafka_publisher import KafkaPublisher
from core.connectors.publishers.s3_publisher import S3Publisher
from core.connectors.publishers.opensearch_publisher import OpenSearchPublisher


class PublishersMetadata(Enum):
    KAFKA = KafkaPublisher
    S3 = S3Publisher
    CONSOLE = ConsolePublisher
    FILE = FilePublisher
    GCS = GCSPublisher
    BIGQUERY = BigQueryPublisher
    OPENSEARCH = OpenSearchPublisher
    # SNOWFLAKE = "snowflake"
    # REDSHIFT = "redshift"


