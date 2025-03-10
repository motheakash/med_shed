from pydantic_settings import BaseSettings


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': 60,  # in minutes
    'REFRESH_TOKEN_LIFETIME': 1,  # in days
    'JWT_ALGORITHM': 'HS256',
    'SECRETE_KEY': 'tokensecretkey',
}

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
