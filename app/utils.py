from datetime import datetime, timedelta

import jwt

from app.config import security_settings


def generate_access_token(
    data: dict,
    expiry: timedelta = timedelta(days=1),
) -> str:
    return jwt.encode(
        payload={
            **data,
            "exp": datetime.now() + expiry,
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET_KEY,
    )


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            key=security_settings.JWT_SECRET_KEY,
            algorithms=[security_settings.JWT_ALGORITHM],
        )
    except jwt.DecodeError:
        return None
