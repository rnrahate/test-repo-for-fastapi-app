from pydantic_settings import BaseSettings
from pathlib import Path
import os
class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = {
        "env_file": Path(__file__).parent.parent / ".env" if os.getenv("ENV") != "production" else None
    }

settings = Settings() # type: ignore

print(settings.database_password, ">>", settings.database_username)