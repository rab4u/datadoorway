from pydantic.main import BaseModel


class JWTModel(BaseModel):
    sub: str
    iat: int
    exp: int
    scopes: str

