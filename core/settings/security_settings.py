from pydantic import (BaseSettings)


class SecuritySettings(BaseSettings):

    security_enable_authorization: bool = True
    authjwt_secret_key: str = 'headers'
    authjwt_public_key: str = None
    authjwt_private_key: str = None
    authjwt_algorithm: str = 'HS256'
    authjwt_decode_issuer: str = None
    authjwt_decode_audience: str = None
    authjwt_decode_leeway: int = 0
    authjwt_decode_algorithms: list = [authjwt_algorithm]
    authjwt_header_name: str = 'Authorization'
    authjwt_header_type: str = 'Bearer'
    exclude_endpoints: list[str] = ['health', 'ready', 'metrics']
