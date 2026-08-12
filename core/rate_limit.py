from collections import defaultdict, deque
from threading import Lock
from time import monotonic

from fastapi import HTTPException, Request, status

from core.config import settings

_attempts: defaultdict[str, deque[float]] = defaultdict(deque)
_lock = Lock()


def _client_key(request: Request) -> str:
    if request.client is not None:
        return request.client.host
    return "unknown"


def limitar_login(request: Request) -> None:
    now = monotonic()
    cutoff = now - settings.LOGIN_RATE_LIMIT_WINDOW_SECONDS
    key = _client_key(request)

    with _lock:
        attempts = _attempts[key]
        while attempts and attempts[0] <= cutoff:
            attempts.popleft()

        if len(attempts) >= settings.LOGIN_RATE_LIMIT_REQUESTS:
            retry_after = max(1, int(attempts[0] - cutoff))
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Muitas tentativas de autenticação. Tente novamente mais tarde.",
                headers={"Retry-After": str(retry_after)},
            )

        attempts.append(now)


def resetar_rate_limit() -> None:
    with _lock:
        _attempts.clear()
