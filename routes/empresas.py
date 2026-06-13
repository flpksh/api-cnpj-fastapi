from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.security import obter_usuario_atual
from database import get_db
from models.usuario import Usuario
from models.empresa import Empresa
from schemas.empresa_schema import EmpresaCreate

router = APIRouter(prefix="/empresas", tags=["Empresas"])


# LISTAR EMPRESAS COM PAGINAÇÃO, FILTROS E ORDENAÇÃO


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

    query = db.query(Empresa).filter(
        Empresa.usuario_id == usuario.id, Empresa.ativo
    )

    # FILTROS

    if cidade:

        query = query.filter(Empresa.cidade.ilike(f"%{cidade}%"))

    if estado:

        query = query.filter(Empresa.estado.ilike(f"%{estado}%"))

    # ORDENAÇÃO

    campos_validos = {
        "id": Empresa.id,
        "nome": Empresa.nome,
        "cnpj": Empresa.cnpj,
        "cidade": Empresa.cidade,
        "estado": Empresa.estado,
    }

    campo = campos_validos.get(ordem, Empresa.id)

    if direcao.lower() == "desc":

        query = query.order_by(campo.desc())

    else:

        query = query.order_by(campo.asc())

    total = query.count()

    empresas = query.offset(skip).limit(limit).all()

    return {
        "success": True,
        "message": "Empresas encontradas",
        "pagination": {"page": page, "limit": limit, "total": total},
        "filters": {"cidade": cidade, "estado": estado},
        "sorting": {"ordem": ordem, "direcao": direcao},
        "data": empresas,
    }


# CRIAR EMPRESA
@router.post("/")
def criar_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):

    nova_empresa = Empresa(
        cnpj=empresa.cnpj,
        nome=empresa.nome,
        cidade=empresa.cidade,
        estado=empresa.estado,
        usuario_id=usuario.id,
    )

    db.add(nova_empresa)

    db.commit()

    db.refresh(nova_empresa)

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

    empresa = (
        db.query(Empresa)
        .filter(Empresa.cnpj == cnpj, Empresa.usuario_id == usuario.id)
        .first()
    )

    if not empresa:

        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    empresa.nome = dados.nome
    empresa.cidade = dados.cidade
    empresa.estado = dados.estado

    empresa.atualizado_em = datetime.utcnow()

    db.commit()

    db.refresh(empresa)

    return {"success": True, "message": "Empresa atualizada", "data": empresa}


# DELETAR EMPRESA
@router.delete("/{cnpj}")
def deletar_empresa(
    cnpj: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):

    empresa = (
        db.query(Empresa)
        .filter(
            Empresa.cnpj == cnpj,
            Empresa.usuario_id == usuario.id,
            Empresa.ativo,
        )
        .first()
    )

    if not empresa:

        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    empresa.ativo = False

    db.commit()

    return {"success": True, "message": "Empresa removida", "data": None}
