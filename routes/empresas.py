from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database import get_db

from core.security import obter_usuario_atual

from models import Usuario
from models import Empresa

from schemas.empresa_schema import EmpresaCreate


router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)


# LISTAR EMPRESAS
@router.get("/")
def listar_empresas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):

    empresas = db.query(
        Empresa
    ).filter(
        Empresa.usuario_id == usuario.id
    ).all()

    return {

        "success": True,

        "message": "Empresas encontradas",

        "data": empresas
    }


# CRIAR EMPRESA
@router.post("/")
def criar_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):

    nova_empresa = Empresa(

        cnpj=empresa.cnpj,
        nome=empresa.nome,
        cidade=empresa.cidade,
        estado=empresa.estado,
        usuario_id=usuario.id
    )

    db.add(nova_empresa)

    db.commit()

    db.refresh(nova_empresa)

    return {

        "success": True,

        "message": "Empresa criada com sucesso",

        "data": nova_empresa
    }


# ATUALIZAR EMPRESA
@router.put("/{cnpj}")
def atualizar_empresa(
    cnpj: str,
    dados: EmpresaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):

    empresa = db.query(
        Empresa
    ).filter(
        Empresa.cnpj == cnpj,
        Empresa.usuario_id == usuario.id
    ).first()

    if not empresa:

        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    empresa.nome = dados.nome
    empresa.cidade = dados.cidade
    empresa.estado = dados.estado

    db.commit()

    db.refresh(empresa)

    return {

        "success": True,

        "message": "Empresa atualizada",

        "data": empresa
    }


# DELETAR EMPRESA
@router.delete("/{cnpj}")
def deletar_empresa(
    cnpj: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):

    empresa = db.query(
        Empresa
    ).filter(
        Empresa.cnpj == cnpj,
        Empresa.usuario_id == usuario.id
    ).first()

    if not empresa:

        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    db.delete(empresa)

    db.commit()

    return {

        "success": True,

        "message": "Empresa removida",

        "data": None
    }
