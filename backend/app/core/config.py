from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ResQGrid"
    app_env: str = "development"

    postgres_db: str = "resqgrid"
    postgres_user: str = "resqgrid"
    postgres_password: str = "resqgrid_dev_password"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    redis_host: str = "localhost"
    redis_port: int = 6379

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}"


settings = Settings()