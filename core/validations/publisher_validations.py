from http import HTTPStatus
from typing import List

from fastapi import HTTPException, Query

from core.settings.settings import PublisherSettings


class PublisherValidations:
    def __init__(self, settings: PublisherSettings):
        """
        Constructor to VerifyPublisher
        **param** settings: Setting Object
        """
        self.settings = settings

    async def __call__(self,
                       publisher: set[str] = Query(default=None,
                                                   description="List of publishers required to publish the data"
                                                   ),
                       backup_publisher: str = Query(
                           None,
                           description="Backup publisher required to publish the data in "
                                       "case of main publisher fails"
                       )):
        """
        Validate the list of publishers
        :param publisher: List of publishers required to publish the data
        :param backup_publisher: Backup publisher required to publish the data in case of main publisher fails
        :exception: HTTPException
        """
        invalid_publishers = publisher.issubset(self.settings.publishers)
        if not invalid_publishers:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Query param is invalid. "
                       f"Allowed publisher values : {self.settings.publishers}"
            )

        if backup_publisher and backup_publisher not in self.settings.publishers:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=f"Query param is invalid. Allowed backup_publisher values:"
                                       f" {self.settings.publishers}")