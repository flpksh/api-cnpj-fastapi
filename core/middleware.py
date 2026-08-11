import re
from collections.abc import Awaitable, Callable
from time import perf_counter
from uuid import uuid4

from fastapi import Request, Response

from core.logger import definir_request_id, logger, restaurar_request_id

REQUEST_ID_HEADER = "X-Request-ID"
REQUEST_ID_VALIDO = re.compile(r"[A-Za-z0-9._-]{1,64}")


def obter_request_id(valor_recebido: str | None) -> str:
    if valor_recebido and REQUEST_ID_VALIDO.fullmatch(valor_recebido):
        return valor_recebido
    return uuid4().hex


async def adicionar_contexto_requisicao(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request_id = obter_request_id(request.headers.get(REQUEST_ID_HEADER))
    token = definir_request_id(request_id)
    inicio = perf_counter()

    try:
        response = await call_next(request)
        duracao_ms = (perf_counter() - inicio) * 1000
        response.headers[REQUEST_ID_HEADER] = request_id
        logger.info(
            "request method=%s path=%s status=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            duracao_ms,
        )
        return response
    except Exception:
        duracao_ms = (perf_counter() - inicio) * 1000
        logger.exception(
            "request_failed method=%s path=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            duracao_ms,
        )
        raise
    finally:
        restaurar_request_id(token)
