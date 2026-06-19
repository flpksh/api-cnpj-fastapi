from sqlalchemy.orm import Session

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
):

    query = empresa_repository.buscar_por_usuario(
        db=db,
        usuario_id=usuario_id,
    )

    if cidade:
        query = query.filter(Empresa.cidade.ilike(f"%{cidade}%"))

    if estado:
        query = query.filter(Empresa.estado.ilike(f"%{estado}%"))

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

    return query


def criar_empresa(
    db: Session,
    dados: EmpresaCreate,
    usuario_id: int,
):

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

    logger.info(f"Empresa criada: {empresa.nome}")

    return resultado


def atualizar_empresa(
    db: Session,
    cnpj: str,
    dados: EmpresaCreate,
    usuario_id: int,
):

    empresa = empresa_repository.buscar_por_cnpj(
        db=db,
        cnpj=cnpj,
        usuario_id=usuario_id,
    )

    if not empresa:

        logger.error(f"Empresa não encontrada: {cnpj}")

        raise EmpresaNaoEncontrada()

    empresa.nome = dados.nome
    empresa.cidade = dados.cidade
    empresa.estado = dados.estado

    empresa_repository.atualizar(db)

    logger.info(f"Empresa atualizada: {cnpj}")

    return empresa


def deletar_empresa(
    db: Session,
    cnpj: str,
    usuario_id: int,
):

    empresa = empresa_repository.buscar_por_cnpj(
        db=db,
        cnpj=cnpj,
        usuario_id=usuario_id,
    )

    if not empresa:

        logger.error(f"Empresa não encontrada: {cnpj}")

        raise EmpresaNaoEncontrada()

    empresa_repository.deletar(
        db=db,
        empresa=empresa,
    )

    logger.warning(f"Empresa removida: {cnpj}")

    return {"mensagem": "Empresa removida"}