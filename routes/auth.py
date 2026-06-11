from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.config import settings
from core.security import criar_token
from database import get_db
from schemas.usuario_schema import UsuarioCreate
from services.auth_service import autenticar_usuario, criar_usuario

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):

    usuario_criado = criar_usuario(db, usuario.username, usuario.senha)

    return {
        "success": True,
        "message": "Usuário criado com sucesso",
        "data": {"id": usuario_criado.id, "username": usuario_criado.username},
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):

    usuario = autenticar_usuario(db, form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = criar_token(
        dados={"sub": usuario.username}, tempo_expiracao=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
