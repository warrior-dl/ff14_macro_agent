from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    database_url: str = "postgresql://postgres:macro123@localhost:5432/macrodb"

    class Config:
        env_file = ".env"

settings = Settings()
