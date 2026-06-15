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

def test_create_empresa_invalid_cnpj(client):
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

    # Tentativa de criar empresa com CNPJ inválido
    response = client.post(
        "/empresas/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "cnpj": "123",
            "nome": "Empresa Inválida",
            "cidade": "Florianópolis",
            "estado": "SC"
        }
    )

    assert response.status_code == 422

    body = response.json()

    assert "detail" in body

def test_create_empresa_duplicate_cnpj(client):
    username = f"user_{uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username,
            "senha": "123456"
        }
    )

    login = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "123456"
        }
    )

    token = login.json()["access_token"]

    payload = {
        "cnpj": "12345678000195",
        "nome": "Empresa Teste",
        "cidade": "Florianópolis",
        "estado": "SC",
    }

    primeira = client.post(
        "/empresas/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json=payload,
    )

    assert primeira.status_code == 200

    segunda = client.post(
        "/empresas/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json=payload,
    )

    assert segunda.status_code == 409

    body = segunda.json()

    assert body["detail"] == "CNPJ já cadastrado"

def test_list_empresas_empty(client):
    username = f"user_{uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username,
            "senha": "123456"
        }
    )

    login = client.post(
        "/auth/login",
        data={
            "username": username,
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

    body = response.json()

    assert body["success"] is True
    assert body["data"] == []
    assert body["pagination"]["total"] == 0

def test_list_empresas_only_owner(client):
    # Usuário A
    username_a = f"user_a_{uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username_a,
            "senha": "123456"
        }
    )

    login_a = client.post(
        "/auth/login",
        data={
            "username": username_a,
            "password": "123456"
        }
    )

    token_a = login_a.json()["access_token"]

    # Empresa do usuário A
    client.post(
        "/empresas/",
        headers={
            "Authorization": f"Bearer {token_a}"
        },
        json={
            "cnpj": "11111111000111",
            "nome": "Empresa A",
            "cidade": "Florianópolis",
            "estado": "SC"
        }
    )

    # Usuário B
    username_b = f"user_b_{uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username_b,
            "senha": "123456"
        }
    )

    login_b = client.post(
        "/auth/login",
        data={
            "username": username_b,
            "password": "123456"
        }
    )

    token_b = login_b.json()["access_token"]

    # Empresa do usuário B
    client.post(
        "/empresas/",
        headers={
            "Authorization": f"Bearer {token_b}"
        },
        json={
            "cnpj": "22222222000122",
            "nome": "Empresa B",
            "cidade": "São Paulo",
            "estado": "SP"
        }
    )

    # Usuário A lista empresas
    response = client.get(
        "/empresas/",
        headers={
            "Authorization": f"Bearer {token_a}"
        }
    )

    assert response.status_code == 200

    body = response.json()

    empresas = body["data"]

    assert len(empresas) == 1
    assert empresas[0]["nome"] == "Empresa A"
    assert empresas[0]["cnpj"] == "11111111000111"

def test_update_empresa_success(client):
    username = f"user_{uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username,
            "senha": "123456"
        }
    )

    login = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "123456"
        }
    )

    token = login.json()["access_token"]

    client.post(
        "/empresas/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "cnpj": "33333333000133",
            "nome": "Empresa Original",
            "cidade": "Florianópolis",
            "estado": "SC"
        }
    )

    response = client.put(
        "/empresas/33333333000133",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "cnpj": "33333333000133",
            "nome": "Empresa Atualizada",
            "cidade": "Joinville",
            "estado": "SC"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Empresa atualizada"

    empresa = body["data"]

    assert empresa["nome"] == "Empresa Atualizada"
    assert empresa["cidade"] == "Joinville"
    assert empresa["estado"] == "SC"

def test_update_empresa_other_user_forbidden(client):
    # Usuário A
    username_a = f"user_a_{uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username_a,
            "senha": "123456"
        }
    )

    login_a = client.post(
        "/auth/login",
        data={
            "username": username_a,
            "password": "123456"
        }
    )

    token_a = login_a.json()["access_token"]

    # Usuário A cria empresa
    client.post(
        "/empresas/",
        headers={
            "Authorization": f"Bearer {token_a}"
        },
        json={
            "cnpj": "44444444000144",
            "nome": "Empresa do Usuário A",
            "cidade": "Florianópolis",
            "estado": "SC"
        }
    )

    # Usuário B
    username_b = f"user_b_{uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username_b,
            "senha": "123456"
        }
    )

    login_b = client.post(
        "/auth/login",
        data={
            "username": username_b,
            "password": "123456"
        }
    )

    token_b = login_b.json()["access_token"]

    # Usuário B tenta atualizar empresa do A
    response = client.put(
        "/empresas/44444444000144",
        headers={
            "Authorization": f"Bearer {token_b}"
        },
        json={
            "cnpj": "44444444000144",
            "nome": "Tentativa de Invasão",
            "cidade": "São Paulo",
            "estado": "SP"
        }
    )

    assert response.status_code == 404

    body = response.json()

    assert body["detail"] == "Empresa não encontrada"


def test_delete_empresa_success(client):
    username = f"user_{uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username,
            "senha": "123456",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "123456",
        },
    )

    token = login.json()["access_token"]

    # cria empresa
    client.post(
        "/empresas/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "cnpj": "55555555000155",
            "nome": "Empresa Delete",
            "cidade": "Florianópolis",
            "estado": "SC",
        },
    )

    # remove empresa
    response = client.delete(
        "/empresas/55555555000155",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Empresa removida"
    assert body["data"] is None


def test_soft_delete_removes_empresa_from_listing(client):
    username = f"user_{uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username,
            "senha": "123456",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "123456",
        },
    )

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "cnpj": "66666666000166",
        "nome": "Empresa Soft Delete",
        "cidade": "Florianópolis",
        "estado": "SC",
    }

    # Cria empresa
    client.post(
        "/empresas/",
        headers=headers,
        json=payload,
    )

    # Confirma que ela aparece na listagem
    antes = client.get(
        "/empresas/",
        headers=headers,
    )

    body_antes = antes.json()

    assert antes.status_code == 200
    assert body_antes["pagination"]["total"] == 1
    assert len(body_antes["data"]) == 1

    # Remove empresa
    delete = client.delete(
        "/empresas/66666666000166",
        headers=headers,
    )

    assert delete.status_code == 200

    # Lista novamente
    depois = client.get(
        "/empresas/",
        headers=headers,
    )

    body_depois = depois.json()

    assert depois.status_code == 200
    assert body_depois["pagination"]["total"] == 0
    assert body_depois["data"] == []


def test_delete_empresa_twice(client):
    username = f"user_{uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username,
            "senha": "123456",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "123456",
        },
    )

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    client.post(
        "/empresas/",
        headers=headers,
        json={
            "cnpj": "77777777000177",
            "nome": "Empresa Delete Twice",
            "cidade": "Florianópolis",
            "estado": "SC",
        },
    )

    primeira = client.delete(
        "/empresas/77777777000177",
        headers=headers,
    )

    assert primeira.status_code == 200

    segunda = client.delete(
        "/empresas/77777777000177",
        headers=headers,
    )

    assert segunda.status_code == 404

    body = segunda.json()

    assert body["detail"] == "Empresa não encontrada"


def test_delete_empresa_other_user_forbidden(client):
    # Usuário A
    username_a = f"user_a_{uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username_a,
            "senha": "123456",
        },
    )

    login_a = client.post(
        "/auth/login",
        data={
            "username": username_a,
            "password": "123456",
        },
    )

    token_a = login_a.json()["access_token"]

    # Empresa do usuário A
    client.post(
        "/empresas/",
        headers={
            "Authorization": f"Bearer {token_a}"
        },
        json={
            "cnpj": "88888888000188",
            "nome": "Empresa do Usuário A",
            "cidade": "Florianópolis",
            "estado": "SC",
        },
    )

    # Usuário B
    username_b = f"user_b_{uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username_b,
            "senha": "123456",
        },
    )

    login_b = client.post(
        "/auth/login",
        data={
            "username": username_b,
            "password": "123456",
        },
    )

    token_b = login_b.json()["access_token"]

    # Usuário B tenta excluir empresa do A
    response = client.delete(
        "/empresas/88888888000188",
        headers={
            "Authorization": f"Bearer {token_b}"
        },
    )

    assert response.status_code == 404

    body = response.json()

    assert body["detail"] == "Empresa não encontrada"


def test_update_empresa_not_found(client):
    username = f"user_{uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username,
            "senha": "123456",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "123456",
        },
    )

    token = login.json()["access_token"]

    response = client.put(
        "/empresas/99999999000199",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "cnpj": "99999999000199",
            "nome": "Empresa Inexistente",
            "cidade": "São Paulo",
            "estado": "SP",
        },
    )

    assert response.status_code == 404

    body = response.json()

    assert body["detail"] == "Empresa não encontrada"