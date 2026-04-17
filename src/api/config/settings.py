from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REGION: str | None = ""
    TABLEAU_SITE_ID: str | None = ""
    USER: str | None = ""
    CLIENT_ID: str | None = ""
    SECRET_ID: str | None = ""
    SECRET_KEY: str | None = ""
    
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()