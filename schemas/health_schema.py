from typing import Literal

from pydantic import BaseModel


class LivenessResponse(BaseModel):
    status: Literal["ok"]


class ReadinessResponse(BaseModel):
    status: Literal["ok"]
    database: Literal["available"]


class ReadinessUnavailableResponse(BaseModel):
    status: Literal["unavailable"]
    database: Literal["unavailable"]
