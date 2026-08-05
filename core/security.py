from datetime import datetime, timedelta, timezone
from typing import Annotated, Any
from uuid import uuid4

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.config import settings
from database import get_db
from models.usuario import Usuario

argon2_hasher = PasswordHasher()
bcrypt_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SENHA_FICTICIA = "senha-ficticia-para-validacao"
HASH_SENHA_FICTICIA = argon2_hasher.hash(SENHA_FICTICIA)


def gerar_hash_senha(senha: str) -> str:
    return argon2_hasher.hash(senha)


def verificar_e_atualizar_senha(
    senha: str,
    senha_hash: str,
) -> tuple[bool, str | None]:
    if senha_hash.startswith("$argon2"):
        try:
            senha_valida = argon2_hasher.verify(senha_hash, senha)
        except (InvalidHashError, VerificationError):
            return False, None

        hash_atualizado = (
            argon2_hasher.hash(senha)
            if argon2_hasher.check_needs_rehash(senha_hash)
            else None
        )
        return senha_valida, hash_atualizado

    if senha_hash.startswith(("$2a$", "$2b$", "$2y$")):
        try:
            bcrypt_valida = bcrypt_context.verify(senha, senha_hash)
        except ValueError:
            return False, None

        return bcrypt_valida, gerar_hash_senha(senha) if bcrypt_valida else None

    return False, None


def criar_token(
    dados: dict[str, Any],
    tempo_expiracao: timedelta | None = None,
) -> str:
    agora = datetime.now(timezone.utc)
    expiracao = agora + (
        tempo_expiracao
        if tempo_expiracao is not None
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    dados_token = {
        **dados,
        "exp": expiracao,
        "iat": agora,
        "jti": uuid4().hex,
    }

    return jwt.encode(
        dados_token,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM,
    )


def _erro_credenciais() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )


def verificar_token(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> str:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM],
            options={"require_exp": True, "require_sub": True},
        )
    except JWTError as erro:
        raise _erro_credenciais() from erro

    username = payload.get("sub")
    if not isinstance(username, str) or not username:
        raise _erro_credenciais()

    return username


def obter_usuario_atual(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> Usuario:
    username = verificar_token(token)
    usuario = db.query(Usuario).filter(Usuario.username == username).first()

    if usuario is None:
        raise _erro_credenciais()

    return usuario
