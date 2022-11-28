from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from requests import Response

from main import app
from tests.constants import JWT_TOKEN

client = TestClient(app)


class TestSchemaEndpoint:
    def test_get_schema_success(self):
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

    def test_get_schema_invalid_format(self):
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

    def test_get_schema_io_error(self):
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

    def test_post_schema_empty(self):
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

    def test_post_schema_invalid(self):
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
        assert response.json() == {'detail': "Schema Validation failed. "
                                             "reason: 'string1' is not valid under any of the given schemas"}

    def test_post_schema_success(self):
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

    def test_post_schema_io_error(self):
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

    def test_validate_success(self):
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

    def test_validate_invalid_schema(self):
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
        assert response.json() == {'detail': "Schema Validation failed. "
                                             "reason: 'number1' is not valid under any of the given schemas"}

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
        assert response.json() == {'detail': 'Data Validation failed. reason: 110 is greater than or equal to the '
                                             'maximum of 100'}
