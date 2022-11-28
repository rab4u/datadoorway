from http import HTTPStatus

from fastapi.testclient import TestClient
from requests import Response

from core.settings.settings import Settings
from core.utilities.basics import get_env_file
from main import app
from tests.constants import JWT_TOKEN

client = TestClient(app)
env_file = get_env_file()
settings = Settings(env_file=env_file)


class TestPublishEndpoint:
    def test_get_publish_success(self):
        response: Response = client.get(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,

            }
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"publishers": list(settings.publisher_publishers)}

    def test_post_publish_without_backup_publisher(self):
        response: Response = client.post(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
            },
            params={
                "publishers": ["kafka", "s3"],
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

    def test_post_publish_invalid_publisher(self):
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

    def test_post_publish_invalid_backup_publisher(self):
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

    def test_post_publish_invalid_data(self):
        response: Response = client.post(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
            },
            params={
                "publishers": ["kafka", "s3"],
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
        assert response.json() == {'detail': 'Data Validation failed. reason: 110 is greater than or equal to '
                                             'the maximum of 100'}
