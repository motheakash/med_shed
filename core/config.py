from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str
    DEBUG: bool
    VERSION: str

    # MongoDB Settings
    MONGO_URI: str
    DATABASE_NAME: str

    # Other Settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"  # Load variables from .env file


settings = Settings()
