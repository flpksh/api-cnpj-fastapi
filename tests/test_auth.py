from uuid import uuid4

def test_register(client):
    username = f"user_test_{uuid4().hex}"

    response = client.post(
        "/auth/register",
        json={
            "username": username,
            "senha": "123456"
        }
    )

    assert response.status_code == 200
    assert "id" in response.json()["data"]

def test_login(client):
    client.post(
        "/auth/register",
        json={
            "username": "user_login",
            "senha": "123456"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "user_login",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_protected_route(client):
    client.post(
        "/auth/register",
        json={
            "username": "user_token",
            "senha": "123456"
        }
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "user_token",
            "password": "123456"
        }
    )

    token = login.json()["access_token"]

    response = client.get(
        "/empresas/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_register_duplicate_user(client):
    username = f"user_{uuid4().hex}"

    response_1 = client.post(
        "/auth/register",
        json={
            "username": username,
            "senha": "123456"
        }
    )

    assert response_1.status_code == 200

    response_2 = client.post(
        "/auth/register",
        json={
            "username": username,
            "senha": "123456"
        }
    )

    assert response_2.status_code == 409


def test_login_invalid_password(client):
    username = f"user_{uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username,
            "senha": "123456"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "senha_errada"
        }
    )

    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        data={
            "username": f"user_{uuid4().hex}",
            "password": "123456"
        }
    )

    assert response.status_code == 401

def test_protected_route_without_token(client):
    response = client.get("/empresas/")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_protected_route_invalid_token(client):
    response = client.get(
        "/empresas/",
        headers={
            "Authorization": "Bearer token_invalido"
        }
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Token inválido"
    }

def test_create_empresa_success(client):
    username = f"user_{uuid4().hex}"

    # Registro
    client.post(
        "/auth/register",
        json={
            "username": username,
            "senha": "123456"
        }
    )

    # Login
    login = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "123456"
        }
    )

    token = login.json()["access_token"]

    # Criação da empresa
    response = client.post(
        "/empresas/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "cnpj": "12345678000195",
            "nome": "Empresa Teste",
            "cidade": "Florianópolis",
            "estado": "SC"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Empresa criada com sucesso"

    empresa = data["data"]

    assert empresa["cnpj"] == "12345678000195"
    assert empresa["nome"] == "Empresa Teste"
    assert empresa["cidade"] == "Florianópolis"
    assert empresa["estado"] == "SC"

    assert "id" in empresa