from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    api_key:str=""
    admin_key:str=""
    allowed_origins:str="*"
    rate_limit_per_minute:int=60
    max_provider_url_age_seconds:int=900
    model_config=SettingsConfigDict(env_file=".env", extra="ignore")
settings=Settings()
