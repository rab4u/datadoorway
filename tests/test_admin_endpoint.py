from http import HTTPStatus

import pytest
from requests import Response
from starlette.testclient import TestClient

from core.settings.settings import Settings
from core.utilities.basics import get_env_file
from main import app
from tests.constants import JWT_TOKEN


class TestAdminEndpoint:
    @pytest.fixture
    def settings(self):
        return Settings(env_file=get_env_file())

    @pytest.fixture
    def client(self):
        with TestClient(app) as c:
            yield c

    def test_get_settings_success(self, client, settings):
        response: Response = client.get(
            url="/admin",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
                "x-admin-secret": settings.security_admin_secret.get_secret_value()

            }
        )
        assert response.status_code == HTTPStatus.OK

    def test_invalid_admin_secret(self, client):
        response: Response = client.get(
            url="/admin",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
                "x-admin-secret": "hello"

            }
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Access denied. Invalid admin secret'}

    def test_get_settings_missing_admin_secret(self, client):
        response: Response = client.get(
            url="/admin",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,

            }
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json() == {'detail': [{'loc': ['header', 'x-admin-secret'], 'msg': 'field required',
                                               'type': 'value_error.missing'}]}

    def test_put_setting_success(self, client, settings):
        response: Response = client.put(
            url="/admin",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
                "x-admin-secret": settings.security_admin_secret.get_secret_value()

            },
            json={
                "key": "SCHEMA_ENABLE_VALIDATIONS",
                "value": True
            }
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'updated_settings': {'SCHEMA_ENABLE_VALIDATIONS': 'True'}}

    def test_put_setting_of_set_type(self, client, settings):
        response: Response = client.put(
            url="/admin",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
                "x-admin-secret": settings.security_admin_secret.get_secret_value()

            },
            json={
                "key": "PUBLISHER_PUBLISHERS",
                "value": ["s3", "bigquery"]
            }
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'updated_settings': {'PUBLISHER_PUBLISHERS': ['s3', 'bigquery']}}

    def test_put_setting_of_list_type(self, client, settings):
        response: Response = client.put(
            url="/admin",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
                "x-admin-secret": settings.security_admin_secret.get_secret_value()

            },
            json={
                "key": "SECURITY_JWT_ALGORITHMS",
                "value": ["HS256", "RS256"]
            }
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'updated_settings': {'SECURITY_JWT_ALGORITHMS': ['HS256', 'RS256']}}

    def test_put_setting_of_secret_type(self, client, settings):
        response: Response = client.put(
            url="/admin",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
                "x-admin-secret": settings.security_admin_secret.get_secret_value()

            },
            json={
                "key": "SECURITY_ADMIN_SECRET",
                "value": "hello_admin"
            }
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'updated_settings': {'SECURITY_ADMIN_SECRET': '**********'}}

    def test_put_setting_invalid(self, client, settings):
        response: Response = client.put(
            url="/admin",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
                "x-admin-secret": settings.security_admin_secret.get_secret_value()

            },
            json={
                "key": "SCHEMA_ENABLE_VALIDATIONS1",
                "value": True
            }
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {'detail': "Key 'SCHEMA_ENABLE_VALIDATIONS1' not found in settings. "
                                             "'Settings' object has no attribute 'schema_enable_validations1'"}
