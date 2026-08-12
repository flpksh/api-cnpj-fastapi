from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.config import settings
from core.rate_limit import limitar_login
from core.security import criar_token
from database import get_db
from schemas.usuario_schema import (
    TokenResponse,
    UsuarioCreate,
    UsuarioCreateResponse,
)
from services.auth_service import autenticar_usuario, criar_usuario

router = APIRouter(prefix="/auth", tags=["Auth"], dependencies=[Depends(limitar_login)])


@router.post("/register", response_model=UsuarioCreateResponse)
def registrar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
):
    usuario_criado = criar_usuario(
        db,
        usuario.username,
        usuario.senha.get_secret_value(),
    )

    return {
        "success": True,
        "message": "Usuário criado com sucesso",
        "data": {"id": usuario_criado.id, "username": usuario_criado.username},
    }


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    username = form_data.username.strip().lower()
    usuario = autenticar_usuario(db, username, form_data.password)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = criar_token(
        dados={"sub": usuario.username},
        tempo_expiracao=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
