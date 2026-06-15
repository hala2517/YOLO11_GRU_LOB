from functools import lru_cache
from typing import Literal

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="Cosmecca API", validation_alias=AliasChoices("APP_NAME"))
    app_version: str = Field(default="0.1.0", validation_alias=AliasChoices("APP_VERSION"))
    app_env: Literal["development", "staging", "production"] = Field(
        default="development",
        validation_alias=AliasChoices("APP_ENV"),
    )
    debug: bool = Field(default=False, validation_alias=AliasChoices("DEBUG"))
    api_v1_str: str = Field(default="/api/v1", validation_alias=AliasChoices("API_V1_STR"))

    host: str = Field(default="0.0.0.0", validation_alias=AliasChoices("HOST"))
    port: int = Field(default=8000, validation_alias=AliasChoices("PORT"))

    database_url: str = Field(
        default="sqlite+aiosqlite:///./cosmecca.db",
        validation_alias=AliasChoices("DATABASE_URL"),
    )
    allowed_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        validation_alias=AliasChoices("ALLOWED_ORIGINS"),
    )

    secret_key: str = Field(
        default="changeme-insecure-secret-key",
        validation_alias=AliasChoices("SECRET_KEY"),
    )
    algorithm: str = Field(default="HS256", validation_alias=AliasChoices("ALGORITHM"))
    access_token_expire_minutes: int = Field(
        default=60 * 24,
        validation_alias=AliasChoices("ACCESS_TOKEN_EXPIRE_MINUTES"),
    )

    cctv_stream_mode: Literal["whep", "hls", "iframe"] = Field(
        default="whep",
        validation_alias=AliasChoices("CCTV_STREAM_MODE"),
    )
    media_mtx_whep_base_url: str = Field(
        default="http://localhost:8889",
        validation_alias=AliasChoices("MEDIA_MTX_WHEP_BASE_URL"),
    )
    media_mtx_rtsp_base_url: str = Field(
        default="rtsp://localhost:8554",
        validation_alias=AliasChoices("MEDIA_MTX_RTSP_BASE_URL"),
    )
    stream_token_expire_seconds: int = Field(
        default=300,
        validation_alias=AliasChoices("STREAM_TOKEN_EXPIRE_SECONDS"),
    )
    stream_idle_timeout_seconds: int = Field(
        default=60,
        validation_alias=AliasChoices("STREAM_IDLE_TIMEOUT_SECONDS"),
    )
    stream_max_concurrent: int = Field(
        default=16,
        validation_alias=AliasChoices("STREAM_MAX_CONCURRENT"),
    )
    ffmpeg_path: str = Field(default="ffmpeg", validation_alias=AliasChoices("FFMPEG_PATH"))
    hls_output_dir: str = Field(default="./var/hls", validation_alias=AliasChoices("HLS_OUTPUT_DIR"))
    hls_public_base_url: str = Field(
        default="/api/v1/streams",
        validation_alias=AliasChoices("HLS_PUBLIC_BASE_URL"),
    )

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
