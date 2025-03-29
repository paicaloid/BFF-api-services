from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    OIDC_ISSUER: str
    OIDC_CLIENT_ID: str
    OIDC_CLIENT_SECRET: str
    OIDC_AUDIENCE: str


settings = Settings()
