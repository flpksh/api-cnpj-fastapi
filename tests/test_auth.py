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
