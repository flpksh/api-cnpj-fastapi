from pydantic import BaseModel, field_validator

class EmpresaBase(BaseModel):
    cnpj: str
    nome: str
    cidade: str
    estado: str

    @field_validator("cnpj")
    def validar_cnpj(cls, v):

        v = ''.join(filter(str.isdigit, v))

        if len(v) != 14:
            raise ValueError("CNPJ deve conter 14 dígitos")

        return v

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaResponse(EmpresaBase):
    id: int

    class Config:
        from_attributes = True
