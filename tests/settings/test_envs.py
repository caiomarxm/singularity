import pytest
from pydantic import ValidationError
from singularity.settings.settings import Settings


def test_invalid_db_target(monkeypatch):
    # Mock environment variables with an invalid SINGULARITY_DB_TARGET
    monkeypatch.setenv("SINGULARITY_DB_TARGET", "invalid_target")
    monkeypatch.setenv("SINGULARITY_DB_HOST", "localhost")
    monkeypatch.setenv("SINGULARITY_DB_PORT", "5432")
    monkeypatch.setenv("SINGULARITY_DB_USER", "user")
    monkeypatch.setenv("SINGULARITY_DB_PASSWORD", "password")

    # Expect ValidationError due to invalid SINGULARITY_DB_TARGET
    with pytest.raises(ValidationError):
        Settings()


def test_valid_postgres_env(monkeypatch):
    # Mock environment variables
    monkeypatch.setenv("SINGULARITY_DB_TARGET", "postgres")
    monkeypatch.setenv("SINGULARITY_DB_HOST", "localhost")
    monkeypatch.setenv("SINGULARITY_DB_PORT", "5432")
    monkeypatch.setenv("SINGULARITY_DB_USER", "user")
    monkeypatch.setenv("SINGULARITY_DB_PASSWORD", "password")
    monkeypatch.setenv("SINGULARITY_DB_NAME", "dummy_db")

    # Initialize settings and assert
    settings = Settings()
    assert settings.SINGULARITY_DB_TARGET == "postgres"
    assert settings.SINGULARITY_DB_HOST == "localhost"
    assert settings.SINGULARITY_DB_PORT == 5432
    assert settings.SINGULARITY_DB_USER == "user"
    assert settings.SINGULARITY_DB_PASSWORD == "password"
    assert settings.SINGULARITY_DB_NAME == "dummy_db"
    assert (
        settings.SINGULARITY_DB_CONNECTION_URL
        == "postgresql+psycopg2://user:password@localhost:5432/dummy_db"
    )


def test_valid_mysql_env(monkeypatch):
    # Mock environment variables
    monkeypatch.setenv("SINGULARITY_DB_TARGET", "mysql")
    monkeypatch.setenv("SINGULARITY_DB_HOST", "localhost")
    monkeypatch.setenv("SINGULARITY_DB_PORT", "3306")
    monkeypatch.setenv("SINGULARITY_DB_USER", "user")
    monkeypatch.setenv("SINGULARITY_DB_PASSWORD", "password")
    monkeypatch.setenv("SINGULARITY_DB_NAME", "dummy_db")

    # Initialize settings and assert
    settings = Settings()
    assert settings.SINGULARITY_DB_TARGET == "mysql"
    assert settings.SINGULARITY_DB_HOST == "localhost"
    assert settings.SINGULARITY_DB_PORT == 3306
    assert settings.SINGULARITY_DB_USER == "user"
    assert settings.SINGULARITY_DB_PASSWORD == "password"
    assert settings.SINGULARITY_DB_NAME == "dummy_db"
    assert (
        settings.SINGULARITY_DB_CONNECTION_URL
        == "mysql+mysqlconnector://user:password@localhost:3306/dummy_db"
    )


def test_valid_sqlite_env(monkeypatch):
    # Mock environment variables
    monkeypatch.setenv("SINGULARITY_DB_TARGET", "sqlite")
    monkeypatch.setenv("SINGULARITY_DB_HOST", "")
    monkeypatch.setenv("SINGULARITY_DB_USER", "")
    monkeypatch.setenv("SINGULARITY_DB_PASSWORD", "")
    monkeypatch.setenv("SINGULARITY_DB_NAME", "dummy_db")

    # Initialize settings and assert
    settings = Settings()
    assert settings.SINGULARITY_DB_TARGET == "sqlite"
    assert settings.SINGULARITY_DB_NAME == "dummy_db"
    assert settings.SINGULARITY_DB_CONNECTION_URL == "sqlite:///./dummy_db.db"
