from datetime import UTC, datetime
from uuid import UUID

import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.exceptions import AuthenticationError, DomainError
from backend.app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from backend.app.models.refresh_token import RefreshToken
from backend.app.models.user import User
from backend.app.models.user_profile import UserProfile
from backend.app.schemas.auth import LoginRequest, RegisterRequest


def register_user(database: Session, payload: RegisterRequest) -> User:
    email = payload.email.lower()
    if database.scalar(select(User).where(User.email == email)) is not None:
        raise DomainError("An account with this email already exists", 409)
    user = User(email=email, password_hash=hash_password(payload.password), display_name=payload.display_name.strip())
    database.add(user)
    database.flush()
    database.add(UserProfile(user_id=user.id))
    database.commit()
    database.refresh(user)
    return user


def authenticate_user(database: Session, payload: LoginRequest) -> User:
    user = database.scalar(select(User).where(User.email == payload.email.lower()))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise AuthenticationError("Invalid email or password")
    if not user.is_active:
        raise AuthenticationError("This account is disabled")
    user.last_login_at = datetime.now(UTC)
    database.commit()
    return user


def issue_tokens(database: Session, user: User) -> tuple[str, str]:
    access = create_access_token(str(user.id))
    refresh, expires_at, jti = create_refresh_token(str(user.id))
    database.add(RefreshToken(user_id=user.id, token_jti=jti, expires_at=expires_at))
    database.commit()
    return access, refresh


def rotate_refresh_token(database: Session, token: str) -> tuple[User, str, str]:
    try:
        payload = decode_token(token, expected_type="refresh")
        user_id = UUID(str(payload["sub"]))
        jti = str(payload["jti"])
    except (ValueError, KeyError, jwt.InvalidTokenError) as exc:
        raise AuthenticationError("Invalid refresh token") from exc

    stored = database.scalar(select(RefreshToken).where(RefreshToken.token_jti == jti))
    if stored is None or stored.revoked or stored.expires_at < datetime.now(UTC):
        raise AuthenticationError("Refresh token has expired or been revoked")
    user = database.scalar(select(User).where(User.id == user_id, User.is_active.is_(True)))
    if user is None:
        raise AuthenticationError("User account is unavailable")
    stored.revoked = True
    database.commit()
    access, refresh = issue_tokens(database, user)
    return user, access, refresh


def revoke_refresh_token(database: Session, token: str) -> None:
    try:
        payload = decode_token(token, expected_type="refresh")
        jti = str(payload["jti"])
    except (KeyError, jwt.InvalidTokenError) as exc:
        raise AuthenticationError("Invalid refresh token") from exc
    stored = database.scalar(select(RefreshToken).where(RefreshToken.token_jti == jti))
    if stored is not None:
        stored.revoked = True
        database.commit()
