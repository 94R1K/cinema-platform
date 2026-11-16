from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class AccessTokenClaims(BaseModel):
    user_id: UUID
    session_id: UUID
    jti: UUID
    type: Literal["access"]
    exp: int
