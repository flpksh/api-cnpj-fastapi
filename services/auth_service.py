from sqlalchemy.orm import Session

from models import Usuario

from core.security import gerar_hash_senha
from core.security import verificar_senha

from core.exceptions import (
    UsuarioJaExiste,
    CredenciaisInvalidas
)

from core.logger import logger


def criar_usuario(
    db: Session,
    username: str,
    senha: str
):

    usuario_existente = db.query(
        Usuario
    ).filter(
        Usuario.username == username
    ).first()

    if usuario_existente:

        logger.warning(
            f"Tentativa de registro com usuário existente: {username}"
        )

        raise UsuarioJaExiste()

    novo_usuario = Usuario(

        username=username,
        senha=gerar_hash_senha(senha)
    )

    db.add(novo_usuario)

    db.commit()

    db.refresh(novo_usuario)

    logger.info(
        f"Usuário criado: {username}"
    )

    return novo_usuario


def autenticar_usuario(
    db: Session,
    username: str,
    senha: str
):

    usuario = db.query(
        Usuario
    ).filter(
        Usuario.username == username
    ).first()

    if not usuario:

        logger.warning(
            f"Tentativa de login inválido: {username}"
        )

        raise CredenciaisInvalidas()

    senha_valida = verificar_senha(
        senha,
        usuario.senha
    )

    if not senha_valida:

        logger.warning(
            f"Senha inválida para usuário: {username}"
        )

        raise CredenciaisInvalidas()

    logger.info(
        f"Login realizado: {username}"
    )

    return usuario
