from core.config import config
from datetime import datetime, timezone
from schemas.security import TokenRequest
from jose import jwt
from passlib.context import CryptContext


def create_access_token(token_request: TokenRequest) -> str:

    payload = {
        "sub": token_request.user_id,
        "exp": datetime.now(timezone.utc) + token_request.expires_delta,
        **token_request.model_dump(exclude={"expires_delta", "user_id"}),
    }

    return jwt.encode(
        payload,
        key=config.security.SECRET_KEY,
        algorithm=config.security.ALGORITHM,
    )


def verify_token(token: str) -> TokenRequest:
    payload = jwt.decode(
        token=token,
        key=config.security.SECRET_KEY,
        algorithms=[config.security.ALGORITHM],
    )

    return payload


bcrypt_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    hashed_password = bcrypt_context.hash(password)

    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    is_valid = bcrypt_context.verify(password, hashed_password)

    return is_valid
