from datetime import timedelta, datetime
from typing import Union
import hashlib
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.models.model import (TokenData, Token, User)
from core.validations.validations import unauthorized
router = APIRouter()


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_EXPIRE_DAYS = 3652  # approx 10 years
TEST_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJjbGllbnRfaWQiOiJ0ZXN0X2NsaWVudCIsImV4cCI6MTk3MjU3OTk1NH0.xvue_RS_Ey1miOtIHelLOWu4rCxW1repvttvYwZlEJs"

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(OAUTH2_SCHEME)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise unauthorized
        token_data = TokenData(username=username)
    except JWTError:
        raise unauthorized
    return User(username=username)


@router.post("/token", response_model=Token)
async def login_for_access_token(sub: str = "test_user", client_id: str = "test_client"):
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    m = hashlib.sha256()
    s = sub.encode('utf-8')
    m.update(s)
    hashed_sub = m.hexdigest()
    print(hashed_sub)
    access_token = create_access_token(
        data={"sub": hashed_sub, "client_id": client_id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


class TokenValidator(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(TokenValidator, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = \
            await super(TokenValidator, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403,
                                    detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403,
                                    detail="Invalid token or expired token.")
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> bool:
        is_valid: bool = False

        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
        except JWTError:
            payload = None
        if payload:
            is_valid = True
        return is_valid