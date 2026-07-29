from pydantic import Field, MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Read automatically from APP_ENV (case-insensitive) or defaults to 'development'
    app_env: str = "development"
    
    # Automatically validated as a valid PostgreSQL connection string
    database_url: MySQLDsn
    test_database_url: MySQLDsn
    
    secret_key: str = Field(description="The secret key for external API authentication")

    model_config = SettingsConfigDict(
        env_file=".env",              # Read from a local .env file
        env_file_encoding="utf-8",    # Encoding for the file
        extra="ignore"                # Silently ignore extra env variables
    )


settings = Settings() # type: ignore[call-arg]
