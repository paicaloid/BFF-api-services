from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    INTERNAL_API_KEY: str

    @computed_field  # type: ignore[misc]
    @property
    def header(self) -> dict[str, str]:
        return {"X-Internal-API-Key": self.INTERNAL_API_KEY}

    LOGIN_SERVICE_URL: str = "localhost"
    LOGIN_SERVICE_PORT: int = 8100

    @computed_field  # type: ignore[misc]
    @property
    def login_url(self) -> str:
        return f"http://{self.LOGIN_SERVICE_URL}:{self.LOGIN_SERVICE_PORT}"

    USER_SERVICE_URL: str = "localhost"
    USER_SERVICE_PORT: int = 8200

    @computed_field  # type: ignore[misc]
    @property
    def user_url(self) -> str:
        return f"http://{self.USER_SERVICE_URL}:{self.USER_SERVICE_PORT}"

    POST_SERVICE_URL: str = "localhost"
    POST_SERVICE_PORT: int = 8300

    @computed_field  # type: ignore[misc]
    @property
    def post_url(self) -> str:
        return f"http://{self.POST_SERVICE_URL}:{self.POST_SERVICE_PORT}"

    OIDC_ISSUER: str
    OIDC_AUDIENCE: str


settings = Settings()
