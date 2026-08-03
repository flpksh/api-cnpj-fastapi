from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.exceptions import EmpresaNaoEncontrada
from core.security import obter_usuario_atual
from database import get_db
from models.usuario import Usuario
from schemas.empresa_schema import (
    CNPJ,
    EmpresaCreate,
    EmpresaDeleteResponse,
    EmpresaListParams,
    EmpresaListResponse,
    EmpresaMutationResponse,
)
from services import empresa_service

router = APIRouter(prefix="/empresas", tags=["Empresas"])


# LISTAR EMPRESAS


@router.get("/", response_model=EmpresaListResponse)
def listar_empresas(
    params: Annotated[EmpresaListParams, Query()],
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    skip = (params.page - 1) * params.limit

    query = empresa_service.listar_empresas(
        db=db,
        usuario_id=usuario.id,
        cidade=params.cidade,
        estado=params.estado,
        ordem=params.ordem,
        direcao=params.direcao,
    )

    total = query.count()
    empresas = query.offset(skip).limit(params.limit).all()

    return {
        "success": True,
        "message": "Empresas encontradas",
        "pagination": {
            "page": params.page,
            "limit": params.limit,
            "total": total,
            "pages": (total + params.limit - 1) // params.limit,
        },
        "filters": {
            "cidade": params.cidade,
            "estado": params.estado,
        },
        "sorting": {
            "ordem": params.ordem,
            "direcao": params.direcao,
        },
        "data": empresas,
    }


# CRIAR EMPRESA


@router.post("/", response_model=EmpresaMutationResponse)
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
        ) from None

    return {
        "success": True,
        "message": "Empresa criada com sucesso",
        "data": nova_empresa,
    }


# ATUALIZAR EMPRESA


@router.put("/{cnpj}", response_model=EmpresaMutationResponse)
def atualizar_empresa(
    cnpj: CNPJ,
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
        ) from None

    return {
        "success": True,
        "message": "Empresa atualizada",
        "data": empresa,
    }


# DELETAR EMPRESA


@router.delete("/{cnpj}", response_model=EmpresaDeleteResponse)
def deletar_empresa(
    cnpj: CNPJ,
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
        ) from None

    return {
        "success": True,
        "message": "Empresa removida",
        "data": None,
    }
