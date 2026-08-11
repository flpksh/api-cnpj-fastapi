import logging

from sqlalchemy.exc import SQLAlchemyError

from core.logger import RequestIdFilter, definir_request_id, restaurar_request_id
from database import get_db
from main import app


class DatabaseIndisponivel:
    def execute(self, statement: object) -> None:
        raise SQLAlchemyError("database indisponível")


def test_liveness_retorna_ok_e_request_id(client) -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert len(response.headers["x-request-id"]) == 32


def test_request_id_valido_e_preservado(client) -> None:
    response = client.get(
        "/health/live",
        headers={"X-Request-ID": "cliente-request-123"},
    )

    assert response.headers["x-request-id"] == "cliente-request-123"


def test_request_id_invalido_e_substituido(client) -> None:
    response = client.get(
        "/health/live",
        headers={"X-Request-ID": "valor invalido com espacos"},
    )

    assert response.headers["x-request-id"] != "valor invalido com espacos"
    assert len(response.headers["x-request-id"]) == 32


def test_readiness_retorna_ok_quando_banco_responde(client) -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "available"}


def test_readiness_retorna_503_quando_banco_falha(client) -> None:
    def override_get_db_indisponivel():
        yield DatabaseIndisponivel()

    app.dependency_overrides[get_db] = override_get_db_indisponivel

    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "unavailable",
        "database": "unavailable",
    }
    assert "x-request-id" in response.headers


def test_logger_inclui_request_id_do_contexto() -> None:
    record = logging.LogRecord(
        name="api_cnpj",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="evento",
        args=(),
        exc_info=None,
    )
    token = definir_request_id("request-log-123")

    try:
        RequestIdFilter().filter(record)
    finally:
        restaurar_request_id(token)

    assert record.request_id == "request-log-123"  # type: ignore[attr-defined]


def test_openapi_documenta_endpoints_de_health(client) -> None:
    schema = client.get("/openapi.json").json()

    assert "/health/live" in schema["paths"]
    assert "/health/ready" in schema["paths"]
    assert "503" in schema["paths"]["/health/ready"]["get"]["responses"]
