from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    LOGIN_SERVICE_URL: str = "localhost"
    LOGIN_SERVICE_PORT: int = 8100

    OIDC_ISSUER: str
    OIDC_AUDIENCE: str


settings = Settings()
