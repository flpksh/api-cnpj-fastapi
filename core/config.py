from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = Field(ge=1, le=65535)
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    SECRET_KEY: SecretStr = Field(min_length=32)
    ALGORITHM: Literal["HS256", "HS384", "HS512"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(gt=0, le=1440)

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @field_validator("SECRET_KEY")
    @classmethod
    def rejeitar_chave_insegura(cls, valor: SecretStr) -> SecretStr:
        if valor.get_secret_value().strip().lower() in {
            "change-me",
            "secret",
            "secret-key",
        }:
            raise ValueError("SECRET_KEY deve ser uma chave aleatória e segura")
        return valor

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )


settings = Settings()  # type: ignore[call-arg]
