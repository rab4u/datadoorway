from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from requests import Response

from main import app
from tests.constants import JWT_TOKEN


class TestSchemaEndpoint:

    @pytest.fixture
    def client(self):
        with TestClient(app) as c:
            yield c

    def test_get_schema_success(self, client):
        response: Response = client.get(
            url="/schema",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,

            },
            params={
                "schema_id": "users/mobile/android"
            }
        )
        assert response.status_code == HTTPStatus.OK

    def test_get_schema_invalid_format(self, client):
        response: Response = client.get(
            url="/schema",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,

            },
            params={
                "schema_id": "users.mobile.android"
            }
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {'detail': 'Query param is invalid. Allowed schema_id format : '
                                             'root/subject/name. Example: users/mobile/ios.json'}

    def test_get_schema_io_error(self, client):
        response: Response = client.get(
            url="/schema",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
            },
            params={
                "schema_id": "users/mobile/android1"
            }
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {'detail': "Invalid schema id. reason: "
                                             "No schema found with the schema id : users/mobile/android1"}

    def test_post_schema_empty(self, client):
        response: Response = client.post(
            url="/schema",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
            },
            params={
                "schema_id": "users/mobile/android"
            },
            json={}
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {'detail': 'Schema Validation failed. reason: Empty schema'}

    def test_post_schema_invalid(self, client):
        response: Response = client.post(
            url="/schema",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
            },
            params={
                "schema_id": "users/mobile/android"
            },
            json={
                "properties": {
                    "age": {
                        "exclusiveMaximum": 100,
                        "minimum": 0,
                        "type": "number"
                    },
                    "created_on": {
                        "format": "date-time",
                        "type": "string1"
                    }
                },
                "type": "object"
            }
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {'detail': "Validation failed. reason: Unknown type: 'string1'"}

    def test_post_schema_success(self, client):
        response: Response = client.post(
            url="/schema",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
            },
            params={
                "schema_id": "users/tmp/v1"
            },
            json={
                "properties": {
                    "age": {
                        "exclusiveMaximum": 100,
                        "minimum": 0,
                        "type": "number"
                    },
                    "created_on": {
                        "format": "date-time",
                        "type": "string"
                    }
                },
                "type": "object"
            }
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'detail': 'Successfully updated the schema with schema id: users/tmp/v1'}

    def test_post_schema_io_error(self, client):
        response: Response = client.post(
            url="/schema",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
            },
            params={
                "schema_id": "users/mobile/v2"
            },
            json={
                "properties": {
                    "age": {
                        "exclusiveMaximum": 100,
                        "minimum": 0,
                        "type": "number"
                    },
                    "created_on": {
                        "format": "date-time",
                        "type": "string"
                    }
                },
                "type": "object"
            }
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {'detail': 'Cannot create / overwrite existing '
                                             'schema with schema_id : users/mobile/v2'}

    def test_validate_success(self, client):
        response: Response = client.post(
            url="/validate",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
            },
            json={
                "json_schema": {
                    "properties": {
                        "age": {
                            "exclusiveMaximum": 100,
                            "minimum": 0,
                            "type": "number"
                        },
                        "created_on": {
                            "format": "date-time",
                            "type": "string"
                        }
                    },
                    "type": "object"
                },
                "data": {
                    "age": 99,
                    "created_on": "2018-11-13T20:20:39+00:00",
                }
            }
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'detail': 'Schema validation is successful'}

    def test_validate_invalid_schema(self, client):
        response: Response = client.post(
            url="/validate",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
            },
            json={
                "json_schema": {
                    "properties": {
                        "age": {
                            "exclusiveMaximum": 100,
                            "minimum": 0,
                            "type": "number1"
                        },
                        "created_on": {
                            "format": "date-time",
                            "type": "string"
                        }
                    },
                    "type": "object"
                },
                "data": {
                    "age": 99,
                    "created_on": "2018-11-13T20:20:39+00:00",
                }
            }
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {'detail': "Validation failed. reason: Unknown type: 'number1'"}

    def test_validate_invalid_data(self, client):
        response: Response = client.post(
            url="/validate",
            headers={
                "accept": "application/json",
                "Authorization": JWT_TOKEN,
            },
            json={
                "json_schema": {
                    "properties": {
                        "age": {
                            "exclusiveMaximum": 100,
                            "minimum": 0,
                            "type": "number"
                        },
                        "created_on": {
                            "format": "date-time",
                            "type": "string"
                        }
                    },
                    "type": "object"
                },
                "data": {
                    "age": 110,
                    "created_on": "2018-11-13T20:20:39+00:00",
                }
            }
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {'detail': 'Validation failed. reason: data.age must be smaller than 100'}
