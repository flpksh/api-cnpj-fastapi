from uuid import uuid4


def test_jornada_completa_usuario(client):

    username = f"user_integracao_{uuid4().hex}"

    registro = client.post(
        "/auth/register", json={"username": username, "senha": "123456"}
    )

    assert registro.status_code == 200

    body = registro.json()

    assert body["success"] is True
    assert "id" in body["data"]

    login = client.post(
        "/auth/login", data={"username": username, "password": "123456"}
    )

    assert login.status_code == 200

    login_body = login.json()

    assert "access_token" in login_body
    assert login_body["token_type"] == "bearer"

    token = login_body["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    empresa = client.post(
        "/empresas/",
        headers=headers,
        json={
            "cnpj": "11111111000111",
            "nome": "Empresa Integração",
            "cidade": "Florianópolis",
            "estado": "SC",
        },
    )

    assert empresa.status_code == 200

    empresa_body = empresa.json()

    assert empresa_body["success"] is True
    assert empresa_body["data"]["cnpj"] == "11111111000111"
    assert empresa_body["data"]["nome"] == "Empresa Integração"

    listagem = client.get("/empresas/", headers=headers)

    assert listagem.status_code == 200

    listagem_body = listagem.json()

    assert listagem_body["pagination"]["total"] == 1

    assert len(listagem_body["data"]) == 1

    assert listagem_body["data"][0]["cnpj"] == "11111111000111"

    atualizacao = client.put(
        "/empresas/11111111000111",
        headers=headers,
        json={
            "cnpj": "11111111000111",
            "nome": "Empresa Atualizada",
            "cidade": "São José",
            "estado": "SC",
        },
    )

    assert atualizacao.status_code == 200

    body_atualizacao = atualizacao.json()

    assert body_atualizacao["data"]["nome"] == "Empresa Atualizada"
    assert body_atualizacao["data"]["cidade"] == "São José"

    delete = client.delete(
        "/empresas/11111111000111",
        headers=headers,
    )

    assert delete.status_code == 200

    listagem_final = client.get("/empresas/", headers=headers)

    assert listagem_final.status_code == 200

    body_final = listagem_final.json()

    assert body_final["pagination"]["total"] == 0
    assert body_final["data"] == []
