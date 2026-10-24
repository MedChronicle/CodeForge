from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_database
from backend.app.core.exceptions import DomainError
from backend.app.models.user import User
from backend.app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse, UserResponse
from backend.app.schemas.common import MessageResponse
from backend.app.services.auth_service import authenticate_user, issue_tokens, register_user, revoke_refresh_token, rotate_refresh_token


router = APIRouter(prefix="/auth", tags=["auth"])


def token_response(user: User, access: str, refresh: str) -> TokenResponse:
    return TokenResponse(access_token=access, refresh_token=refresh, user=UserResponse.model_validate(user))


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, database: Session = Depends(get_database)) -> TokenResponse:
    user = register_user(database, payload)
    access, refresh = issue_tokens(database, user)
    return token_response(user, access, refresh)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, database: Session = Depends(get_database)) -> TokenResponse:
    user = authenticate_user(database, payload)
    access, refresh = issue_tokens(database, user)
    return token_response(user, access, refresh)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, database: Session = Depends(get_database)) -> TokenResponse:
    user, access, refresh_token = rotate_refresh_token(database, payload.refresh_token)
    return token_response(user, access, refresh_token)


@router.post("/logout", response_model=MessageResponse)
def logout(payload: RefreshRequest, database: Session = Depends(get_database)) -> MessageResponse:
    revoke_refresh_token(database, payload.refresh_token)
    return MessageResponse(message="Signed out")


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(user)
