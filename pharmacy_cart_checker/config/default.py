from os import environ

from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    """

    ENV: str = environ.get("ENV", "local")
    PATH_PREFIX: str = environ.get("PATH_PREFIX", "/api/v1")
    APP_HOST: str = environ.get("APP_HOST", "http://127.0.0.1")
    APP_PORT: int = int(environ.get("APP_PORT", 8080))

    DATABASE_CONTAINER: str = environ.get("DATABASE_CONTAINER", "pharmacy_db")
    DATABASE_NAME: str = environ.get("DATABASE_NAME", "pharmacy")
    DATABASE_HOST: str = environ.get("DATABASE_HOST", "localhost")
    DATABASE_USERNAME: str = environ.get("DATABASE_USERNAME", "student")
    DATABASE_PORT: int = int(environ.get("DATABASE_PORT", 5432))
    DATABASE_PASSWORD: str = environ.get("DATABASE_PASSWORD", "shbr202")
    DB_CONNECT_RETRY: int = environ.get("DB_CONNECT_RETRY", 20)
    DB_POOL_SIZE: int = environ.get("DB_POOL_SIZE", 15)

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.DATABASE_NAME,
            "user": self.DATABASE_USERNAME,
            "password": self.DATABASE_PASSWORD,
            "host": self.DATABASE_HOST,
            "port": self.DATABASE_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
