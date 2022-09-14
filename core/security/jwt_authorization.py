from fastapi_jwt_auth import AuthJWT

from core.settings.security_settings import SecuritySettings


class JWTAuthorization:
    def __init__(self, settings: SecuritySettings):
        """
        Constructor for JWTAuthorization
        :param settings: security settings to configure JWT Authorization
        """
        self.settings = settings
        self.authJWT = AuthJWT()

        # callback to get your configuration
        @AuthJWT.load_config
        def get_config():
            return self.settings

    @staticmethod
    def print_settings():
        print(AuthJWT.__dict__)
