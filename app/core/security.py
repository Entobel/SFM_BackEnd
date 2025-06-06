from datetime import datetime, timezone

from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.core.config import config
from app.domain.value_objects.token_payload import TokenPayload

from app.core.exception import AuthenticationError


def create_access_token(token_request: TokenPayload) -> str:
    data = token_request.to_payload()

    payload = {
        "sub": str(token_request.user_id),
        "exp": datetime.now(timezone.utc) + token_request.expires_delta,
        **data,
    }

    return jwt.encode(
        payload,
        key=config.security.SECRET_KEY,
        algorithm=config.security.ALGORITHM,
    )


def verify_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token=token,
            key=config.security.SECRET_KEY,
            algorithms=[config.security.ALGORITHM],
        )

        return payload
    except ExpiredSignatureError as e:
        raise AuthenticationError(error_code="ETB-het_han_token")
    except JWTError as e:
        raise AuthenticationError(error_code="ETB-loi_token")


bcrypt_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    hashed_password = bcrypt_context.hash(password)

    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    is_valid = bcrypt_context.verify(password, hashed_password)

    return is_valid
