from authx import AuthX, AuthXConfig
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.security import HTTPBearer 

class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

jwt_settings = JWTSettings()

class AuthConfig:
    _config = AuthXConfig(
        JWT_SECRET_KEY = jwt_settings.JWT_SECRET_KEY,
        JWT_ALGORITHM = jwt_settings.JWT_ALGORITHM,
        JWT_ACCESS_TOKEN_EXPIRES = jwt_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        JWT_TOKEN_LOCATION=["headers"]
    )

    secure = AuthX(config=_config)

class Bearer_scheme:
    bearer_scheme = HTTPBearer()

authx_service = AuthConfig.secure
bearer_scheme = Bearer_scheme.bearer_scheme
