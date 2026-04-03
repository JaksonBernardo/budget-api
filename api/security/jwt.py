from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from jwt.exceptions import InvalidTokenError

from api.core.settings import Settings

_settings = Settings()


def create_access_token(subject: int) -> str:
    """Gera um JWT token com o user_id como subject."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=_settings.JWT_EXPIRATION_MINUTES)
    payload = {
        "sub": str(subject),
        "exp": expire,
        "type": "access"
    }
    return jwt.encode(payload, _settings.JWT_SECRET_KEY, algorithm=_settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[int]:
    """Decodifica o JWT e retorna o user_id (sub) ou None se inválido."""
    try:
        payload = jwt.decode(
            token,
            _settings.JWT_SECRET_KEY,
            algorithms=[_settings.JWT_ALGORITHM]
        )
        if payload.get("type") != "access":
            return None
        sub = payload.get("sub")
        if sub is None:
            return None
        return int(sub)
    except (InvalidTokenError, ValueError):
        return None
