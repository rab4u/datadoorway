from typing import Dict, List, Union

import awswrangler as wr
import pandas as pd


class AWSWrangler():

    def __init__(self, default_partition: str):
        self._wrangler = wr
        self._default_partitions = ["year", "month", "day"]
        self._partition_type = default_partition
        self._s3_partitions_cols = {
            "default": self._default_partitions,
            "hour": self._default_partitions + ["hour"],
            "minute": self._default_partitions + ["hour", "minute"],
            "second": self._default_partitions + ["hour", "minute", "second"]}
        self._partition_format = {
            "year": "%Y",
            "month": "%m",
            "day": "%d",
            "hour": "%H",
            "minute": "%M",
            "second": "%S"}

    def _pandas_as_dict(self, payload_dict: Dict) -> pd.DataFrame:
        """
        Preparing Payload data as pandas for AWS SDK for Pandas
        :param payload_dict: Payload Data
        :type payload_dict: dict
        :return:
        :rtype:
        """
        df = pd.DataFrame.from_dict([payload_dict])
        df["timestamp"] = pd.to_datetime('now', utc=True)
        for col in self._s3_partitions_cols[self._partition_type]:
            df[col] = df["timestamp"].dt.strftime(self._partition_format.get(col))
        return df

    def _generate_params(self, payload_dict: Dict, s3_bucket: str, s3_path: str) -> Dict:
        """
        Generate Params for Wrangler Data writes
        :param payload_dict: Payload Data
        :type payload_dict: dict
        :param s3_bucket: Destination bucket
        :type s3_bucket: str
        :param s3_path: Destination bucket path
        :type s3_path: str
        :return: wrangler parameters
        :rtype: dict
        """
        return {
            'df': self._pandas_as_dict(payload_dict=payload_dict),
            'dataset': True,
            'path': f"s3://{s3_bucket}/{s3_path}/",
            's3_additional_kwargs': {
                "ACL": "bucket-owner-full-control"},
            "partition_cols": self._s3_partitions_cols[self._partition_type]}

    def save_to_s3(
            self,
            payload_dict: Dict,
            s3_bucket: str,
            s3_path: str,
            partition_type: str = None
    ) -> Dict[str, Union[List[str], Dict[str, List[str]]]]:
        """
        Saving file to S3
        :param payload_dict: Payload Data
        :type payload_dict: dict
        :param s3_bucket: Destination bucket
        :type s3_bucket: str
        :param s3_path: Destination bucket path
        :type s3_path: str
        :param partition_type: Kind of partition to store data in S3
        :type partition_type: str
        :return: Response of Wrangler
        :rtype:
        """
        self._partition_type = partition_type if partition_type else self._partition_type
        return wr.s3.to_parquet(**self._generate_params(payload_dict=payload_dict, s3_bucket=s3_bucket, s3_path=s3_path))
