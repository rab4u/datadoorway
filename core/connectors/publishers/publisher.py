from fastapi import Header, HTTPException
from http import HTTPStatus

from core.settings.publisher_settings import PublisherSettings


class Publisher:
    def __init__(self):
        """
        Constructor for Publisher class
        """