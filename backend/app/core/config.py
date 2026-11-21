import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "ParcelTrack API")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")

    # SQLite Database URL (defaults to local parceltrack.db)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./parceltrack.db")

    # CORS origins permitted for local frontend development
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


settings = Settings()
