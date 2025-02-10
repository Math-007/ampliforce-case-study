from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    redis_host: str
    clickhouse_host: str

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore[call-arg]
