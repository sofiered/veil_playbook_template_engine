from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    base_json_name: str
    data_path: str

    class Config:
        env_file = ".env"

settings = Settings()