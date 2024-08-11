from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    base_json_name: str
    root: str = ''
    main_page_cache_ttl: int

    class Config:
        env_file = ".env"
        extra = 'ignore'


settings = Settings()