from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.logger import logger
from database import get_db
from schemas.health_schema import (
    LivenessResponse,
    ReadinessResponse,
    ReadinessUnavailableResponse,
)

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live", response_model=LivenessResponse)
def verificar_liveness() -> dict[str, str]:
    return {"status": "ok"}


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    responses={503: {"model": ReadinessUnavailableResponse}},
)
def verificar_readiness(
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, str] | JSONResponse:
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.warning("readiness database=unavailable")
        return JSONResponse(
            status_code=503,
            content={"status": "unavailable", "database": "unavailable"},
        )

    return {"status": "ok", "database": "available"}
