import http
from typing import Annotated

from core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError

from api.schemas import AccessTokenClaims


def decode_token(token: str) -> AccessTokenClaims | None:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_public_key,
            algorithms=[settings.jwt_algorithm],
        )
        return AccessTokenClaims.model_validate(payload)
    except JWTError, ValidationError:
        return None


bearer_scheme = HTTPBearer()


class JWTBearer:
    """Dependency для извлечения и декодирования JWT."""

    async def __call__(
        self,
        credentials: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(bearer_scheme),
        ],
    ) -> AccessTokenClaims:
        if credentials is None:
            raise HTTPException(
                status_code=http.HTTPStatus.UNAUTHORIZED,
                detail="Авторизация не выполнена.",
            )

        decoded_token = decode_token(credentials.credentials)

        if decoded_token is None:
            raise HTTPException(
                status_code=http.HTTPStatus.UNAUTHORIZED,
                detail="Недопустимый или просроченный токен.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return decoded_token


security_jwt = JWTBearer()

UserDependency = Annotated[AccessTokenClaims, Depends(security_jwt)]
