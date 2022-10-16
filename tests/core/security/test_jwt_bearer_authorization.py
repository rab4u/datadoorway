from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from requests import Response

from main import app, settings

client = TestClient(app)


@pytest.fixture
def enable_authorization() -> str:
    return "skip" if settings.security_enable_authorization else "run"


skip_by_fixture = pytest.mark.skipif("enable_authorization == 'skip'")


class TestJWTBearerAuthorization:
    @skip_by_fixture
    def test_no_authorization_header(self):

        response: Response = client.get(
            url="/publish",
            headers={
                "accept": "application/json",
            }
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == {'detail': 'Not authenticated'}

    @skip_by_fixture
    def test_invalid_token(self):
        response: Response = client.get(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": "Hello world"
            }
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == {'detail': 'Invalid authentication credentials'}

    @skip_by_fixture
    def test_token_expired(self):
        response: Response = client.get(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                                 "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaW"
                                 "F0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyMzkwMjIsInNjb3BlIjoiZGQ6YWRtaW"
                                 "4gcHVibGlzaDp3cml0ZSBtZXRyaWNzOnJlYWQifQ."
                                 "-AMDe0WXzvDZLWO4tqKHJeDJhSS7PGznQU_mZupftR0"
            }
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Exception raised while decoding JWT token. Details: '
                                             'Signature has expired'}

    @skip_by_fixture
    def test_token_missing_scopes(self):
        response: Response = client.get(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI"
                                 "xMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5"
                                 "MDIyLCJleHAiOjE2NjYyMjQwMDB9.eHY3BxsU8FaXx_e73vLwfYEtvMfJPIzF0m_OwKDdN_I"
            }
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Exception raised while decoding JWT token. Details: Missing JWT scope'}

    @skip_by_fixture
    def test_token_invalid_scopes(self):
        response: Response = client.get(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                                 "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gR"
                                 "G9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2NjYyMj"
                                 "QwMDAsInNjb3BlIjoiZGQ6YWRtaW4gaGVsbG86aGVsbG8i"
                                 "fQ.djBYJuy1pu6KKWBTl_KovPRDMK4wW1jPXZM27fBuBvY"
            }
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': f"Exception raised while decoding JWT token. Invalid JWT scope. Allowed "
                                             f"JWT scopes: {settings.security_jwt_scopes}"}

    @skip_by_fixture
    def test_token_invalid_scopes(self):
        response: Response = client.get(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                                 "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gR"
                                 "G9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2NjYyMj"
                                 "QwMDAsInNjb3BlIjoiZGQ6YWRtaW4gaGVsbG86aGVsbG8i"
                                 "fQ.djBYJuy1pu6KKWBTl_KovPRDMK4wW1jPXZM27fBuBvY"
            }
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': f"Exception raised while decoding JWT token. Invalid JWT scope. Allowed "
                                             f"JWT scopes: {settings.security_jwt_scopes}"}

    @skip_by_fixture
    def test_insufficient_permissions(self):
        response: Response = client.get(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                                 "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9l"
                                 "IiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2NjYyMjQwMDAsInNjb"
                                 "3BlIjoibWV0cmljczpyZWFkIn0.Pf2_phpvJt5p05_V_k80rm74eHszd4izsEymLN6PHEg"
            }
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Exception raised while decoding JWT token. Insufficient permissions'}

    @skip_by_fixture
    def test_auth_success(self):
        response: Response = client.get(
            url="/publish",
            headers={
                "accept": "application/json",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                 ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4g"
                                 "RG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2NjYyMj"
                                 "QwMDAsInNjb3BlIjoiZGQ6cmVhZCJ9.D2n4IjBLsXkkO"
                                 "E6YV8uQ084-eKn6cntvAmqLdPoxgso"
            }
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'publishers': list(settings.publisher_publishers)}
