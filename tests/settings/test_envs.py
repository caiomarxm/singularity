import pytest
from pydantic import ValidationError
from singularity.settings.settings import Settings


def test_valid_env(monkeypatch):
    # Mock environment variables
    monkeypatch.setenv("SINGULARITY_DB_TARGET", "postgres")
    monkeypatch.setenv("SINGULARITY_DB_HOST", "localhost")
    monkeypatch.setenv("SINGULARITY_DB_PORT", "5432")
    monkeypatch.setenv("SINGULARITY_DB_USER", "user")
    monkeypatch.setenv("SINGULARITY_DB_PASSWORD", "password")

    # Initialize settings and assert
    settings = Settings()
    assert settings.SINGULARITY_DB_TARGET == "postgres"
    assert settings.SINGULARITY_DB_HOST == "localhost"
    assert settings.SINGULARITY_DB_PORT == 5432
    assert settings.SINGULARITY_DB_USER == "user"
    assert settings.SINGULARITY_DB_PASSWORD == "password"


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
