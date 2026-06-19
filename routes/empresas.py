from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.exceptions import EmpresaNaoEncontrada
from core.security import obter_usuario_atual
from database import get_db
from models.usuario import Usuario
from schemas.empresa_schema import EmpresaCreate
from services import empresa_service

router = APIRouter(prefix="/empresas", tags=["Empresas"])


# LISTAR EMPRESAS


@router.get("/")
def listar_empresas(
    page: int = 1,
    limit: int = 10,
    cidade: str | None = None,
    estado: str | None = None,
    ordem: str = "id",
    direcao: str = "asc",
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):

    skip = (page - 1) * limit

    query = empresa_service.listar_empresas(
        db=db,
        usuario_id=usuario.id,
        cidade=cidade,
        estado=estado,
        ordem=ordem,
        direcao=direcao,
    )

    total = query.count()

    empresas = query.offset(skip).limit(limit).all()

    return {
        "success": True,
        "message": "Empresas encontradas",
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
        },
        "filters": {
            "cidade": cidade,
            "estado": estado,
        },
        "sorting": {
            "ordem": ordem,
            "direcao": direcao,
        },
        "data": empresas,
    }


# CRIAR EMPRESA


@router.post("/")
def criar_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):

    try:

        nova_empresa = empresa_service.criar_empresa(
            db=db,
            dados=empresa,
            usuario_id=usuario.id,
        )

    except IntegrityError:

        raise HTTPException(
            status_code=409,
            detail="CNPJ já cadastrado",
        )

    return {
        "success": True,
        "message": "Empresa criada com sucesso",
        "data": nova_empresa,
    }


# ATUALIZAR EMPRESA


@router.put("/{cnpj}")
def atualizar_empresa(
    cnpj: str,
    dados: EmpresaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):

    try:

        empresa = empresa_service.atualizar_empresa(
            db=db,
            cnpj=cnpj,
            dados=dados,
            usuario_id=usuario.id,
        )

    except EmpresaNaoEncontrada:

        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada",
        )

    return {
        "success": True,
        "message": "Empresa atualizada",
        "data": empresa,
    }


# DELETAR EMPRESA


@router.delete("/{cnpj}")
def deletar_empresa(
    cnpj: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):

    try:

        empresa_service.deletar_empresa(
            db=db,
            cnpj=cnpj,
            usuario_id=usuario.id,
        )

    except EmpresaNaoEncontrada:

        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada",
        )

    return {
        "success": True,
        "message": "Empresa removida",
        "data": None,
    }