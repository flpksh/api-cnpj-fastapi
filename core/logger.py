import logging
from contextvars import ContextVar, Token

REQUEST_ID_AUSENTE = "-"
_request_id: ContextVar[str] = ContextVar(
    "request_id",
    default=REQUEST_ID_AUSENTE,
)


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = _request_id.get()  # type: ignore[attr-defined]
        return True


def definir_request_id(request_id: str) -> Token[str]:
    return _request_id.set(request_id)


def restaurar_request_id(token: Token[str]) -> None:
    _request_id.reset(token)


logger = logging.getLogger("api_cnpj")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.addFilter(RequestIdFilter())
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s level=%(levelname)s logger=%(name)s "
            "request_id=%(request_id)s %(message)s"
        )
    )
    logger.addHandler(handler)
