import logging
from typing import Literal, Optional
from pydantic import ValidationError, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    SINGULARITY_DB_TARGET: Literal["postgres", "mysql", "sqlite"] = "sqlite"
    SINGULARITY_DB_HOST: str
    SINGULARITY_DB_PORT: Optional[int] = None
    SINGULARITY_DB_USER: str
    SINGULARITY_DB_PASSWORD: str
    SINGULARITY_DB_NAME: str = "singularity"

    @computed_field(return_type=str)
    @property
    def SINGULARITY_DB_CONNECTION_URL(self) -> str:
        def generate_base_conn_url(connector: str):
            return (
                f"{connector}://{self.SINGULARITY_DB_USER}:"
                f"{self.SINGULARITY_DB_PASSWORD}@"
                f"{self.SINGULARITY_DB_HOST}:"
                f"{self.SINGULARITY_DB_PORT}/"
                f"{self.SINGULARITY_DB_NAME}"
            )

        match self.SINGULARITY_DB_TARGET:
            case "mysql":
                return generate_base_conn_url(connector="mysql+mysqlconnector")
            case "postgres":
                return generate_base_conn_url(connector="postgresql+psycopg2")
            case "sqlite":
                return f"sqlite:///./{self.SINGULARITY_DB_NAME}.db"
            case _:
                raise ValueError("Unsupported database type")

    JWT_SECRET_KEY: str
    JWT_EXPIRES_IN_DAYS: int
    JWT_ALGORITHM: str = "HS256"

    FIRST_SUPERUSER_NAME: str
    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_PASSWORD: str


try:
    settings = Settings()
except ValidationError as err:
    logging.error(
        "Settings object could not be generated, please check if your environments meet the '.env.example'."
    )
    logging.error("Full stacktrace bellow:")
    logging.error(str(err.with_traceback(None)))
    raise
