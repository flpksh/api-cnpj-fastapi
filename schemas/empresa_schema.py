from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict

from core.cnpj import validar_cnpj

CNPJ = Annotated[str, BeforeValidator(validar_cnpj)]


class EmpresaBase(BaseModel):
    cnpj: CNPJ
    nome: str
    cidade: str
    estado: str


class EmpresaCreate(EmpresaBase):
    pass


class EmpresaResponse(EmpresaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
