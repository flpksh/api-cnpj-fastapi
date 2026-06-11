from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.config import settings
from database import get_db
from models import Usuario

# ==========================================
# HASH DE SENHA
# ==========================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==========================================
# OAUTH2
# ==========================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# ==========================================
# GERAR HASH
# ==========================================


def gerar_hash_senha(senha: str):

    return pwd_context.hash(senha)


# ==========================================
# VALIDAR SENHA
# ==========================================


def verificar_senha(senha: str, senha_hash: str):

    return pwd_context.verify(senha, senha_hash)


# ==========================================
# CRIAR TOKEN JWT
# ==========================================


def criar_token(dados: dict, tempo_expiracao: timedelta | None = None):

    dados_token = dados.copy()

    if tempo_expiracao:

        expire = datetime.utcnow() + tempo_expiracao

    else:

        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    dados_token.update({"exp": expire})

    token = jwt.encode(dados_token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return token


# ==========================================
# VALIDAR TOKEN
# ==========================================


def verificar_token(token: str = Depends(oauth2_scheme)):

    credenciais_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:

            raise credenciais_exception

        return username

    except JWTError as e:
        
        raise credenciais_exception from e


# ==========================================
# USUÁRIO ATUAL
# ==========================================


def obter_usuario_atual(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):

    credenciais_exception = HTTPException(status_code=401, detail="Token inválido")

    try:

        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:

            raise credenciais_exception

    except JWTError as e:

        raise credenciais_exception from e

    usuario = db.query(Usuario).filter(Usuario.username == username).first()

    if usuario is None:

        raise credenciais_exception

    return usuario
