from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_key: str = ""
    allowed_origins: str = "*"
    rate_limit_per_minute: int = 300
    upstream_download_url: str = ""
    upstream_api_key: str = ""
    upstream_timeout_seconds: int = 120
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
