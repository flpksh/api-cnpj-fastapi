from datetime import timedelta

import jwt
import pytest
from passlib.context import CryptContext
from pydantic import SecretStr, ValidationError

from core.config import Settings, settings
from core.security import criar_token
from models.usuario import Usuario
from schemas.usuario_schema import UsuarioCreate


@pytest.mark.parametrize(
    "senha",
    [
        "curta",
        "a" * 73,
        "á" * 37,
    ],
)
def test_cadastro_rejeita_senha_fora_dos_limites(senha: str) -> None:
    with pytest.raises(ValidationError, match="Senha"):
        UsuarioCreate(username="usuario_teste", senha=SecretStr(senha))


@pytest.mark.parametrize(
    "username",
    [
        "ab",
        "usuario com espaco",
        "usuario@dominio",
        "a" * 51,
    ],
)
def test_cadastro_rejeita_username_invalido(username: str) -> None:
    with pytest.raises(ValidationError):
        UsuarioCreate(username=username, senha=SecretStr("senha-segura-123"))


def test_cadastro_normaliza_username(client) -> None:
    response = client.post(
        "/auth/register",
        json={"username": "  Usuario.Teste  ", "senha": "senha-segura-123"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["username"] == "usuario.teste"

    login = client.post(
        "/auth/login",
        data={"username": " USUARIO.TESTE ", "password": "senha-segura-123"},
    )
    assert login.status_code == 200


def test_novo_usuario_usa_argon2id(client, db) -> None:
    client.post(
        "/auth/register",
        json={"username": "usuario_argon2", "senha": "senha-segura-123"},
    )

    usuario = db.query(Usuario).filter(Usuario.username == "usuario_argon2").one()
    assert usuario.senha.startswith("$argon2id$")


def test_login_atualiza_hash_bcrypt_legado(client, db) -> None:
    bcrypt = CryptContext(schemes=["bcrypt"])
    usuario = Usuario(
        username="Usuario.Legado",
        senha=bcrypt.hash("123456"),
    )
    db.add(usuario)
    db.commit()

    response = client.post(
        "/auth/login",
        data={"username": "usuario.legado", "password": "123456"},
    )

    assert response.status_code == 200
    db.refresh(usuario)
    assert usuario.senha.startswith("$argon2id$")


def test_token_inclui_claims_de_seguranca() -> None:
    token = criar_token({"sub": "usuario_token"})
    payload = jwt.decode(
        token,
        settings.SECRET_KEY.get_secret_value(),
        algorithms=[settings.ALGORITHM],
    )

    assert payload["sub"] == "usuario_token"
    assert isinstance(payload["exp"], int)
    assert isinstance(payload["iat"], int)
    assert isinstance(payload["jti"], str)
    assert payload["jti"]


@pytest.mark.parametrize(
    "token",
    [
        criar_token({}),
        criar_token({"sub": "usuario"}, timedelta(seconds=-1)),
    ],
)
def test_rota_protegida_rejeita_token_sem_sub_ou_expirado(client, token: str) -> None:
    response = client.get(
        "/empresas/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Token inválido"}
    assert response.headers["www-authenticate"] == "Bearer"


def test_login_com_senha_acima_do_limite_retorna_erro_generico(client) -> None:
    response = client.post(
        "/auth/login",
        data={"username": "inexistente", "password": "a" * 73},
    )

    assert response.status_code == 401
    assert response.json()["message"] == "Usuário ou senha inválidos"


@pytest.mark.parametrize(
    "config_invalida",
    [
        {"SECRET_KEY": "chave-curta"},
        {"ACCESS_TOKEN_EXPIRE_MINUTES": 0},
        {"ACCESS_TOKEN_EXPIRE_MINUTES": 1441},
        {"ALGORITHM": "none"},
    ],
)
def test_configuracao_rejeita_valores_inseguros(
    config_invalida: dict[str, object],
) -> None:
    dados: dict[str, object] = {
        "DB_HOST": "localhost",
        "DB_PORT": 5432,
        "DB_USER": "postgres",
        "DB_PASSWORD": "postgres",
        "DB_NAME": "cnpj_db",
        "SECRET_KEY": "test-only-secret-key-with-at-least-32-chars",
        "ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": 30,
        "_env_file": None,
    }
    dados.update(config_invalida)

    with pytest.raises(ValidationError):
        Settings(**dados)  # type: ignore[arg-type]
