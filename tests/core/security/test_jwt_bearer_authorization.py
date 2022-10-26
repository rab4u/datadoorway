from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from requests import Response

from main import app, settings

client = TestClient(app)


class TestJWTBearerAuthorization:

    def test_no_authorization_header(self):
        if settings.security_enable_authorization:
            response: Response = client.get(
                url="/publish",
                headers={
                    "accept": "application/json",
                }
            )
            assert response.status_code == HTTPStatus.FORBIDDEN
            assert response.json() == {'detail': 'Not authenticated'}
        else:
            assert True

    def test_invalid_token(self):
        if settings.security_enable_authorization:
            response: Response = client.get(
                url="/publish",
                headers={
                    "accept": "application/json",
                    "Authorization": "Hello world"
                }
            )
            assert response.status_code == HTTPStatus.FORBIDDEN
            assert response.json() == {'detail': 'Invalid authentication credentials'}
        else:
            assert True

    def test_token_expired(self):
        if settings.security_enable_authorization:
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
        else:
            assert True

    def test_token_missing_scopes(self):
        if settings.security_enable_authorization and settings.security_enable_scopes:
            response: Response = client.get(
                url="/publish",
                headers={
                    "accept": "application/json",
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NT"
                                     "Y3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE5MTky"
                                     "NTk2MjF9.xeA29AOtT5jSuSU06JDc71PK0yG1CU2GLI96B3q_uPA"
                }
            )
            assert response.status_code == HTTPStatus.UNAUTHORIZED
            assert response.json() == {'detail': 'Exception raised while decoding '
                                                 'JWT token. Details: Missing JWT scopes'}
        else:
            assert True

    def test_token_missing_sub(self):
        if settings.security_enable_authorization:
            response: Response = client.get(
                url="/publish",
                headers={
                    "accept": "application/json",
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSm9ob"
                                     "iBEb2UiLCJpYXQiOjE1MTYyMzkwMjIsImV4cCI6MTkxOTI1OTYyMSwic2NvcGVz"
                                     "IjoicHVibGlzaDp3cml0ZSBtZXRyaWNzOmdldCJ9.0wClkLJ_Z-b"
                                     "hRc1ytWSTuaHPEoTW5FMa3ge3M7osyeE"
                }
            )
            assert response.status_code == HTTPStatus.UNAUTHORIZED
            assert response.json() == {'detail': "Exception raised while decoding JWT token. Details: "
                                                 "Missing 'sub' in token"}
        else:
            assert True

    def test_token_missing_exp(self):
        if settings.security_enable_authorization:
            response: Response = client.get(
                url="/publish",
                headers={
                    "accept": "application/json",
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ey"
                                     "JzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0I"
                                     "joxNTE2MjM5MDIyLCJzY29wZXMiOiJwdWJsaXNoOndyaXRlIG1ldHJpY3M6Z2V0In0"
                                     ".9Qhf-rY4m84QcrKOUQyX54ziM0FxHqx7rn71iwE1_4g"
                }
            )
            assert response.status_code == HTTPStatus.UNAUTHORIZED
            assert response.json() == {'detail': "Exception raised while decoding JWT token. Details: "
                                                 "Missing 'exp' in token"}
        else:
            assert True

    def test_token_invalid_scopes_format(self):
        if settings.security_enable_authorization and settings.security_enable_scopes:
            response: Response = client.get(
                url="/publish",
                headers={
                    "accept": "application/json",
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY"
                                     "3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE5MTky"
                                     "NTk2MjEsInNjb3BlcyI6InB1Ymxpc2gkd3JpdGUgbWV0cmljcyNnZXQifQ.hXUGFXE_p"
                                     "7yyGMbWdWPHOlugttgo-dgC4LUN9H88ggY"
                }
            )
            assert response.status_code == HTTPStatus.UNAUTHORIZED
            assert response.json() == {'detail': "Exception raised while decoding JWT token. Allowed "
                                                 "JWT scopes format:'<endpoint>:<role> <endpoint>:<role> "
                                                 "<endpoint>:<role> ...'. Example: 'user:read user:write'"}
        else:
            assert True

    def test_insufficient_permissions(self):
        if settings.security_enable_authorization and settings.security_enable_scopes:
            response: Response = client.get(
                url="/publish",
                headers={
                    "accept": "application/json",
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMj"
                                     "M0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJl"
                                     "eHAiOjE5MTkyNTk2MjEsInNjb3BlcyI6InB1Ymxpc2g6d3JpdGUgbWV0cmljczpn"
                                     "ZXQifQ.-KfavBvcPpJKBdW8Nv5b04ksh9sjTiSCQy9-i9YT4jc"
                }
            )
            assert response.status_code == HTTPStatus.UNAUTHORIZED
            assert response.json() == {'detail': 'Exception raised while decoding JWT token. Insufficient permissions'}
        else:
            assert True

    def test_auth_success(self):
        if settings.security_enable_authorization:
            response: Response = client.get(
                url="/publish",
                headers={
                    "accept": "application/json",
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxM"
                                     "jM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyL"
                                     "CJleHAiOjE5MTkyNjQ0MjYsInNjb3BlcyI6ImRkOmFkbWluIHB1Ymxpc2g6d3Jp"
                                     "dGUgbWV0cmljczpyZWFkIn0.mDKbgFAPQJ-TfZv55ZVp-Bg4f6_6u9mLQRE2hhLn3Z0"
                }
            )
            assert response.status_code == HTTPStatus.OK
            assert response.json() == {'publishers': list(settings.publisher_publishers)}
        else:
            assert True
