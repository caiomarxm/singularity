import logging
from typing import Literal
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    SINGULARITY_DB_TARGET: Literal["postgres", "mysql"]
    SINGULARITY_DB_HOST: str
    SINGULARITY_DB_PORT: int
    SINGULARITY_DB_USER: str
    SINGULARITY_DB_PASSWORD: str


try:
    settings = Settings()
except ValidationError as err:
    logging.error(
        "Settings object could not be generated, please check if your environments meet the '.env.example'."
    )
    logging.error("Full stacktrace bellow:")
    logging.error(str(err.with_traceback(None)))
