from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    version: str = Field(examples=["0.1.0"])
    environment: str = Field(examples=["local"])
