import os
from typing import Optional, Union, Any
from pydantic import PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import tzinfo
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from pathlib import Path

# Esta línea busca el .env un nivel arriba de /core
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

print("POSTGRES_PORT cargado desde .env:", os.environ.get("POSTGRES_PORT"))



class Settings(BaseSettings):
    # Leer los valores de un archivo .env en la carpeta raiz del proyecto
    # model_config = SettingsConfigDict(
    #     env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    # )

    PROFILE: str = "LOCAL"
    CONTEXT_API: str = "/sofia"
    PROJECT_NAME: str = "sofia"
    VERSION: str = "1.0.0"
    TAG: str = "1.0.0"
    LOG_LEVEL: str = "DEBUG"
    # TIMEZONE: tzinfo = ZoneInfo("America/Mexico_City")
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_PORT: Optional[int] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    SQLALCHEMY_DATABASE_URI: Union[Optional[PostgresDsn], Optional[str]] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="after")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            print("Loading SQLALCHEMY_DATABASE_URI from .docker.env file ...")
            return v
        print("Creating SQLALCHEMY_DATABASE_URI from .env file ...")

        # print(f'host={values.data.get("POSTGRES_SERVER")}')
        username=os.environ.get("POSTGRES_USER")
        password=os.environ.get("POSTGRES_PASSWORD")
        host=os.environ.get("POSTGRES_SERVER")
        port=int(os.environ.get("POSTGRES_PORT"))
        path=f"{os.environ.get('POSTGRES_DB') or ''}"
        return PostgresDsn.build(
            scheme="postgresql",
            username=username,
            password=password,
            host=host,
            port=port,
            path=path,
            # username=values.data.get("POSTGRES_USER"),
            # password=values.data.get("POSTGRES_PASSWORD"),
            # host=values.data.get("POSTGRES_SERVER"),
            # port=values.data.get("POSTGRES_PORT"),
            # path=f"{values.data.get('POSTGRES_DB') or ''}",
        )


settings = Settings()
