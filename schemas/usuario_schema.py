from typing import Literal

from pydantic import BaseModel, Field, SecretStr, field_validator

MINIMO_CARACTERES_SENHA = 15
MAXIMO_BYTES_SENHA = 72


class UsuarioCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-z0-9._-]+$",
    )
    senha: SecretStr

    @field_validator("username", mode="before")
    @classmethod
    def normalizar_username(cls, valor: object) -> object:
        return valor.strip().lower() if isinstance(valor, str) else valor

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, valor: SecretStr) -> SecretStr:
        senha = valor.get_secret_value()

        if len(senha) < MINIMO_CARACTERES_SENHA:
            raise ValueError(
                f"Senha deve conter pelo menos {MINIMO_CARACTERES_SENHA} caracteres"
            )

        if len(senha.encode("utf-8")) > MAXIMO_BYTES_SENHA:
            raise ValueError(f"Senha deve conter no máximo {MAXIMO_BYTES_SENHA} bytes")

        return valor


class UsuarioResponse(BaseModel):
    id: int
    username: str


class UsuarioCreateResponse(BaseModel):
    success: Literal[True]
    message: str
    data: UsuarioResponse


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]
