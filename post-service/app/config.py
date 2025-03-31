from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    MSSQL_HOST: str
    MSSQL_USER: str = "sa"
    SA_PASSWORD: str
    MSSQL_DB: str

    INTERNAL_API_KEY: str


settings = Settings()
