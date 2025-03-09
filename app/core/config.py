import inflect
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

class ApiV1PrefixConfig(BaseModel):
    api: str = "/v1"

class ApiPrefixConfig(BaseModel):
    api: str = "/api"
    v1: ApiV1PrefixConfig = ApiV1PrefixConfig()

class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config =SettingsConfigDict(
        env_file=".env",
        env_prefix="APP__",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    db: DataBaseConfig
    run: RunConfig = RunConfig()
    api: ApiV1PrefixConfig = ApiPrefixConfig()

settings = Settings()