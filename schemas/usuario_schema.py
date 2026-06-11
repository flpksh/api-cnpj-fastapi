from pydantic import BaseModel


class UsuarioCreate(BaseModel):
    username: str
    senha: str


class UsuarioLogin(BaseModel):
    username: str
    senha: str
