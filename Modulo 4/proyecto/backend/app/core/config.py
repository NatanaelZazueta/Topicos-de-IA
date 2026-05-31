from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FaceRec EDU"
    VERSION:  str = "1.0.0"
    SECRET_KEY: str = "cambia-esto-por-una-clave-segura-de-64-caracteres"
    ALGORITHM:  str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = "postgresql+asyncpg://postgres:CN010903AZ!@localhost:5432/Estudiantes"
    EMBEDDINGS_PATH: str = r"C:\Users\Christian\Downloads\Reconocimiento_Facial_ITC\dataset\embeddings.pkl"
    THRESHOLD: float = 0.50

    class Config:
        env_file = ".env"

settings = Settings()