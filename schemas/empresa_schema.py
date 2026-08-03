from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, field_validator

from core.cnpj import validar_cnpj

CNPJ = Annotated[str, BeforeValidator(validar_cnpj)]
OrdemEmpresa = Literal["id", "nome", "cnpj", "cidade", "estado"]
DirecaoOrdenacao = Literal["asc", "desc"]


class EmpresaListParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
    cidade: str | None = Field(default=None, min_length=1, max_length=100)
    estado: str | None = Field(default=None, pattern=r"^[A-Z]{2}$")
    ordem: OrdemEmpresa = "id"
    direcao: DirecaoOrdenacao = "asc"

    @field_validator("cidade", mode="before")
    @classmethod
    def normalizar_cidade(cls, valor: object) -> object:
        return valor.strip() if isinstance(valor, str) else valor

    @field_validator("estado", mode="before")
    @classmethod
    def normalizar_estado(cls, valor: object) -> object:
        return valor.strip().upper() if isinstance(valor, str) else valor


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


class PaginacaoResponse(BaseModel):
    page: int
    limit: int
    total: int
    pages: int


class FiltrosEmpresaResponse(BaseModel):
    cidade: str | None
    estado: str | None


class OrdenacaoEmpresaResponse(BaseModel):
    ordem: OrdemEmpresa
    direcao: DirecaoOrdenacao


class EmpresaListResponse(BaseModel):
    success: Literal[True]
    message: str
    pagination: PaginacaoResponse
    filters: FiltrosEmpresaResponse
    sorting: OrdenacaoEmpresaResponse
    data: list[EmpresaResponse]


class EmpresaMutationResponse(BaseModel):
    success: Literal[True]
    message: str
    data: EmpresaResponse


class EmpresaDeleteResponse(BaseModel):
    success: Literal[True]
    message: str
    data: None
