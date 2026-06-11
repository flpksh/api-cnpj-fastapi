from sqlalchemy.orm import Session

from core.exceptions import EmpresaNaoEncontrada
from core.logger import logger
from models.empresa import Empresa
from repositories import empresa_repository
from schemas.empresa_schema import EmpresaCreate


def listar_empresas(db: Session, usuario_id: int):

    return empresa_repository.buscar_por_usuario(db, usuario_id)


def criar_empresa(db: Session, dados: EmpresaCreate, usuario_id: int):

    empresa = Empresa(
        cnpj=dados.cnpj,
        nome=dados.nome,
        cidade=dados.cidade,
        estado=dados.estado,
        usuario_id=usuario_id,
    )

    resultado = empresa_repository.criar(db, empresa)

    logger.info(f"Empresa criada: {empresa.nome}")

    return resultado


def deletar_empresa(db: Session, cnpj: str, usuario_id: int):

    empresa = empresa_repository.buscar_por_cnpj(db, cnpj, usuario_id)

    if not empresa:

        logger.error(f"Empresa não encontrada: {cnpj}")

        raise EmpresaNaoEncontrada()

    logger.warning(f"Empresa removida: {cnpj}")

    empresa_repository.deletar(db, empresa)

    return {"mensagem": "Empresa removida"}
