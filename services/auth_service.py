from typing import cast

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.exceptions import CredenciaisInvalidas, UsuarioJaExiste
from core.logger import logger
from core.security import (
    HASH_SENHA_FICTICIA,
    SENHA_FICTICIA,
    gerar_hash_senha,
    verificar_e_atualizar_senha,
)
from models import Usuario

MAXIMO_BYTES_SENHA = 72


def criar_usuario(
    db: Session,
    username: str,
    senha: str,
) -> Usuario:
    usuario_existente = (
        db.query(Usuario)
        .filter(func.lower(Usuario.username) == username.lower())
        .first()
    )

    if usuario_existente:
        logger.warning("Tentativa de registro com usuário existente")
        raise UsuarioJaExiste()

    novo_usuario = Usuario(username=username, senha=gerar_hash_senha(senha))
    db.add(novo_usuario)

    try:
        db.commit()
    except IntegrityError as erro:
        db.rollback()
        logger.warning("Conflito ao registrar usuário")
        raise UsuarioJaExiste() from erro

    db.refresh(novo_usuario)
    logger.info("Usuário criado id=%s", novo_usuario.id)

    return novo_usuario


def autenticar_usuario(
    db: Session,
    username: str,
    senha: str,
) -> Usuario:
    usuario = (
        db.query(Usuario)
        .filter(func.lower(Usuario.username) == username.lower())
        .first()
    )
    senha_excede_limite = len(senha.encode("utf-8")) > MAXIMO_BYTES_SENHA

    senha_para_verificacao = SENHA_FICTICIA if senha_excede_limite else senha
    hash_para_verificacao = (
        cast(str, usuario.senha) if usuario is not None else HASH_SENHA_FICTICIA
    )
    senha_valida, hash_atualizado = verificar_e_atualizar_senha(
        senha_para_verificacao,
        hash_para_verificacao,
    )

    if usuario is None or senha_excede_limite or not senha_valida:
        logger.warning("Tentativa de login com credenciais inválidas")
        raise CredenciaisInvalidas()

    if hash_atualizado is not None:
        usuario.senha = hash_atualizado
        db.commit()
        db.refresh(usuario)

    logger.info("Login realizado usuario_id=%s", usuario.id)
    return usuario
