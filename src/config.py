from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str = ""  # خليناه اختياري لحد ما تحسموا الـ LLM

    model_config = SettingsConfigDict(env_file=".env")

def get_settings():
    return Settings()