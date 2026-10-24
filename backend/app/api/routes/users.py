from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_database
from backend.app.models.user import User
from backend.app.models.user_profile import UserProfile
from backend.app.schemas.auth import UserResponse
from backend.app.schemas.onboarding import OnboardingRequest, ProfileResponse
from backend.app.schemas.user import UserSettingsUpdate
from backend.app.services.user_service import complete_onboarding, get_or_create_profile, update_settings


router = APIRouter(prefix="/users", tags=["users"])


def profile_response(profile: UserProfile) -> ProfileResponse:
    return ProfileResponse(
        experience_level=profile.experience_level,
        self_ratings=profile.self_ratings,
        preferred_languages=profile.preferred_languages,
        goal=profile.goal,
        timeline_days=profile.timeline_days,
        daily_minutes=profile.daily_minutes,
        mastery=profile.mastery,
        xp=profile.xp,
        level=profile.level,
        current_streak=profile.current_streak,
        longest_streak=profile.longest_streak,
        onboarding_complete=profile.onboarding_complete,
    )


@router.get("/me", response_model=UserResponse)
def current_user(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(user)


@router.get("/me/profile", response_model=ProfileResponse)
def get_profile(user: User = Depends(get_current_user), database: Session = Depends(get_database)) -> ProfileResponse:
    return profile_response(get_or_create_profile(database, user.id))


@router.post("/me/onboarding", response_model=ProfileResponse)
def onboarding(
    payload: OnboardingRequest,
    user: User = Depends(get_current_user),
    database: Session = Depends(get_database),
) -> ProfileResponse:
    return profile_response(complete_onboarding(database, user, payload))


@router.patch("/me/settings", response_model=ProfileResponse)
def settings(
    payload: UserSettingsUpdate,
    user: User = Depends(get_current_user),
    database: Session = Depends(get_database),
) -> ProfileResponse:
    return profile_response(update_settings(database, user, payload))
