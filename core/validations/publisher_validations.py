from http import HTTPStatus

from fastapi import HTTPException, Query
from pydantic import Required

from core.settings.settings import PublisherSettings


class PublisherValidations:
    def __init__(self, settings: PublisherSettings):
        """
        Constructor to VerifyPublisher
        :param settings: PublisherSettings Object
        """
        self.settings = settings

    async def __call__(self,
                       publishers: set[str] = Query(default=Required,
                                                    description="List of publishers required to publish the data"
                                                    ),
                       backup_publisher: str = Query(
                           None,
                           description="Backup publisher required to publish the data in "
                                       "case of main publisher fails"
                       )):
        """
        Validate the list of publishers
        :param publishers: List of publishers required to publish the data
        :param backup_publisher: Backup publisher required to publish the data in case of main publisher fails
        :exception: HTTPException
        """
        invalid = publishers.issubset(self.settings.publisher_publishers)
        if not invalid:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Query param is invalid. "
                       f"Provide publisher values : {publishers}. "
                       f"Allowed publisher values : {self.settings.publisher_publishers}"
            )

        if backup_publisher and backup_publisher not in self.settings.publisher_publishers:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=f"Query param is invalid."
                                       f" Provided backup_publisher value: {backup_publisher}. "
                                       f" Allowed backup_publisher values: {self.settings.publisher_publishers}"
                                )
