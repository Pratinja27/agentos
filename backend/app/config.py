from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "AgentOS"
    database_url: str = "sqlite:///./agentos.db"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    chroma_dir: str = "./data/chroma"
    chroma_enabled: bool = False
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:8080"


settings = Settings()
