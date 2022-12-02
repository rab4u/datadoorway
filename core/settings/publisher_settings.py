from pydantic import BaseSettings, SecretStr


class PublisherSettings(BaseSettings):
    # General publisher settings
    publisher_publishers: set[str] = {"console", "file", "s3", "gcs", "bigquery"}
    # Kafka publisher settings
    publisher_kafka_bootstrap_servers: str | list[str] = 'localhost:29092'
    publisher_kafka_client_id: str = "dd"
    publisher_kafka_metadata_max_age_ms: int = 300000
    publisher_kafka_request_timeout_ms: int = 40000
    publisher_kafka_api_version: str = 'auto'
    publisher_kafka_acks: int | str = 'all'
    publisher_kafka_compression_type: str = None
    publisher_kafka_max_batch_size: int = 16384
    publisher_kafka_max_request_size: int = 1048576
    publisher_kafka_linger_ms: int = 0
    publisher_kafka_send_backoff_ms: int = 100
    publisher_kafka_retry_backoff_ms: int = 100
    publisher_kafka_security_protocol: str = 'PLAINTEXT'
    publisher_kafka_connections_max_idle_ms: int = 540000
    publisher_kafka_enable_idempotence: bool = False
    publisher_kafka_transaction_timeout_ms: int = 60000
    publisher_kafka_sasl_mechanism: str = 'PLAIN'
    publisher_kafka_sasl_plain_password: SecretStr = None
    publisher_kafka_sasl_plain_username: str = None
    publisher_kafka_sasl_kerberos_service_name: str = 'kafka'
    publisher_kafka_sasl_kerberos_domain_name: str = None
    # S3 publisher settings
    publisher_s3_default_partition: str = 'default'


