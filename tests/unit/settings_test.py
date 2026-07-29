import pytest
from pydantic import ValidationError
from pydantic_settings import BaseSettings

from settings import Settings


@pytest.fixture
def mock_valid_env(monkeypatch):
    """Fixture to set up valid environment variables for testing."""
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("DATABASE_URL", "mysql://user:pass@localhost:3306/db")
    monkeypatch.setenv("TEST_DATABASE_URL", "mysql://user:pass@localhost:3306/db_test")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")


def test_settings_load_successfully(mock_valid_env):
    """Test that valid env variables are successfully parsed and coerced."""
    # Force settings to ignore the local .env file during tests 
    # by explicitly overriding _env_file
    settings = Settings(_env_file=None)
    
    assert settings.app_env == "testing"
    assert settings.secret_key == "test-secret-key"
    assert settings.database_url.host == "localhost"
    assert settings.database_url.port == 3306
    assert settings.test_database_url.host == "localhost"
    assert settings.test_database_url.port == 3306


def test_settings_missing_required_fields(monkeypatch):
    """Test that a ValidationError is raised if required fields are missing."""
    monkeypatch.setenv("APP_ENV", "testing")
    # DATABASE_URL and SECRET_KEY are deliberately omitted
    
    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None)
    
    # Verify that the missing fields caused the error
    assert "database_url" in str(exc_info.value)
    assert "secret_key" in str(exc_info.value)


def test_settings_invalid_mysql_url(monkeypatch):
    """Test that MySQLDsn catches invalid database connection strings."""
    monkeypatch.setenv("DATABASE_URL", "postgres://wrong-driver:5432/db") # Wrong driver
    monkeypatch.setenv("SECRET_KEY", "some-key")
    
    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None)
        
    assert "database_url" in str(exc_info.value)
    assert "mysql+" in str(exc_info.value)
