from uuid import uuid4

import pytest


def autenticar(client) -> dict[str, str]:
    username = f"user_contract_{uuid4().hex}"
    client.post(
        "/auth/register",
        json={"username": username, "senha": "senha-segura-123"},
    )
    login = client.post(
        "/auth/login",
        data={"username": username, "password": "senha-segura-123"},
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


@pytest.mark.parametrize(
    "query",
    [
        "page=0",
        "page=-1",
        "limit=0",
        "limit=101",
        "ordem=criado_em",
        "direcao=aleatoria",
        "estado=S",
        "cidade=%20%20",
        "desconhecido=valor",
    ],
)
def test_listagem_rejeita_parametros_invalidos(client, query: str) -> None:
    response = client.get(
        f"/empresas/?{query}",
        headers=autenticar(client),
    )

    assert response.status_code == 422


def test_listagem_normaliza_filtros_e_informa_total_de_paginas(client) -> None:
    headers = autenticar(client)

    for cnpj, nome in [
        ("11111111000191", "Empresa B"),
        ("22222222000191", "Empresa A"),
    ]:
        response = client.post(
            "/empresas/",
            headers=headers,
            json={
                "cnpj": cnpj,
                "nome": nome,
                "cidade": "Florianópolis",
                "estado": "SC",
            },
        )
        assert response.status_code == 200

    response = client.get(
        "/empresas/?page=1&limit=1&cidade=%20Florian%C3%B3polis%20&estado=sc"
        "&ordem=nome&direcao=asc",
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["pagination"] == {"page": 1, "limit": 1, "total": 2, "pages": 2}
    assert body["filters"] == {"cidade": "Florianópolis", "estado": "SC"}
    assert body["sorting"] == {"ordem": "nome", "direcao": "asc"}
    assert body["data"][0]["nome"] == "Empresa A"


@pytest.mark.parametrize(
    ("path", "method", "response_model"),
    [
        ("/empresas/", "get", "EmpresaListResponse"),
        ("/empresas/", "post", "EmpresaMutationResponse"),
        ("/empresas/{cnpj}", "put", "EmpresaMutationResponse"),
        ("/empresas/{cnpj}", "delete", "EmpresaDeleteResponse"),
    ],
)
def test_openapi_documenta_respostas_de_empresas(
    client,
    path: str,
    method: str,
    response_model: str,
) -> None:
    schema = client.get("/openapi.json").json()
    response_schema = schema["paths"][path][method]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]

    assert response_schema["$ref"].endswith(f"/{response_model}")
