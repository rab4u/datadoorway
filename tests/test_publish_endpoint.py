from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from requests import Response

from core.settings.settings import Settings
from core.utilities.basics import get_env_file
from main import app
from tests.constants import JWT_TOKEN


class TestPublishEndpoint:

    @pytest.fixture
    def settings(self):
        return Settings(env_file=get_env_file())

    @pytest.fixture
    def client(self):
        with TestClient(app) as c:
            yield c
            
    def test_get_publish_success(self, client, settings):
        response: Response = client.get(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,

            }
        )
        assert response.status_code == HTTPStatus.OK

    def test_post_publish_without_backup_publisher(self, client):
        response: Response = client.post(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
            },
            params={
                "publishers": ["s3", "bigquery"],
                "schema_id": "users/mobile/android",
                "event_category": "mobile"
            },
            json={
                "age": 99,
                "name": "ravi",
                "email": "rab4@engineer.com",
                "created_on": "2018-11-13T20:20:39+00:00",
                "mobile_number": "123456789"
            }
        )
        assert response.status_code == HTTPStatus.OK

    def test_post_publish_invalid_publisher(self, client):
        response: Response = client.post(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
            },
            params={
                "publishers": ["kafka1", "s3"],
                "schema_id": "users/mobile/android"
            },
            json={
                "age": 99,
                "name": "ravi",
                "email": "rab4@engineer.com",
                "created_on": "2018-11-13T20:20:39+00:00",
                "mobile_number": "123456789"
            }
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_post_publish_invalid_backup_publisher(self, client):
        response: Response = client.post(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
            },
            params={
                "publishers": ["kafka", "s3"],
                "schema_id": "users/mobile/android",
                "backup_publisher": "s3a"
            },
            json={
                "age": 99,
                "name": "ravi",
                "email": "rab4@engineer.com",
                "created_on": "2018-11-13T20:20:39+00:00",
                "mobile_number": "123456789"
            }
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_post_publish_invalid_data(self, client):
        response: Response = client.post(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
            },
            params={
                "publishers": ["bigquery", "s3"],
                "schema_id": "users/mobile/android",
            },
            json={
                "age": 110,
                "name": "ravi",
                "email": "rab4@engineer.com",
                "created_on": "2018-11-13T20:20:39+00:00",
                "mobile_number": "123456789"
            }
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {'detail': 'Validation failed. reason: data.age must be smaller than 100'}
