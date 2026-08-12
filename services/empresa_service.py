from typing import Any

from sqlalchemy.orm import InstrumentedAttribute, Query, Session

from core.exceptions import EmpresaNaoEncontrada
from core.logger import logger
from models.empresa import Empresa
from repositories import empresa_repository
from schemas.empresa_schema import EmpresaCreate


def listar_empresas(
    db: Session,
    usuario_id: int,
    cidade: str | None = None,
    estado: str | None = None,
    ordem: str = "id",
    direcao: str = "asc",
) -> Query[Empresa]:
    query = empresa_repository.buscar_por_usuario(
        db=db,
        usuario_id=usuario_id,
    )

    if cidade:
        query = query.filter(
            Empresa.cidade.ilike(f"%{cidade}%"),
        )

    if estado:
        query = query.filter(
            Empresa.estado.ilike(f"%{estado}%"),
        )

    campos_validos: dict[str, InstrumentedAttribute[Any]] = {
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

    return query


def criar_empresa(
    db: Session,
    dados: EmpresaCreate,
    usuario_id: int,
) -> Empresa:
    empresa = Empresa(
        cnpj=dados.cnpj,
        nome=dados.nome,
        cidade=dados.cidade,
        estado=dados.estado,
        usuario_id=usuario_id,
    )

    resultado = empresa_repository.criar(
        db=db,
        empresa=empresa,
    )

    logger.info("Empresa criada id=%s usuario_id=%s", resultado.id, usuario_id)

    return resultado


def atualizar_empresa(
    db: Session,
    cnpj: str,
    dados: EmpresaCreate,
    usuario_id: int,
) -> Empresa:
    empresa = empresa_repository.buscar_por_cnpj(
        db=db,
        cnpj=cnpj,
        usuario_id=usuario_id,
    )

    if empresa is None:
        logger.warning("Empresa não encontrada usuario_id=%s", usuario_id)
        raise EmpresaNaoEncontrada()

    empresa.nome = dados.nome
    empresa.cidade = dados.cidade
    empresa.estado = dados.estado

    resultado = empresa_repository.atualizar(
        db=db,
        empresa=empresa,
    )

    logger.info("Empresa atualizada id=%s usuario_id=%s", resultado.id, usuario_id)

    return resultado


def deletar_empresa(
    db: Session,
    cnpj: str,
    usuario_id: int,
) -> dict[str, str]:
    empresa = empresa_repository.buscar_por_cnpj(
        db=db,
        cnpj=cnpj,
        usuario_id=usuario_id,
    )

    if empresa is None:
        logger.warning("Empresa não encontrada usuario_id=%s", usuario_id)
        raise EmpresaNaoEncontrada()

    empresa_repository.deletar(
        db=db,
        empresa=empresa,
    )

    logger.info("Empresa removida id=%s usuario_id=%s", empresa.id, usuario_id)

    return {"mensagem": "Empresa removida"}
