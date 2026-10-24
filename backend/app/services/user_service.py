from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.exceptions import NotFoundError
from backend.app.models.user import User
from backend.app.models.user_profile import UserProfile
from backend.app.schemas.onboarding import OnboardingRequest
from backend.app.schemas.sheet import SheetGenerateRequest
from backend.app.schemas.user import UserSettingsUpdate
from backend.app.services.sheet_service import generate_sheet
from backend.ml.skill_estimator import estimate_mastery


def get_or_create_profile(database: Session, user_id) -> UserProfile:
    profile = database.scalar(select(UserProfile).where(UserProfile.user_id == user_id))
    if profile is None:
        if database.scalar(select(User.id).where(User.id == user_id)) is None:
            raise NotFoundError("User not found")
        profile = UserProfile(user_id=user_id)
        database.add(profile)
        database.commit()
        database.refresh(profile)
    return profile


def complete_onboarding(database: Session, user: User, payload: OnboardingRequest) -> UserProfile:
    profile = get_or_create_profile(database, user.id)
    profile.experience_level = payload.experience_level
    profile.self_ratings = payload.self_ratings
    profile.preferred_languages = payload.preferred_languages
    profile.goal = payload.goal
    profile.timeline_days = payload.timeline_days
    profile.daily_minutes = payload.daily_minutes
    profile.mastery = estimate_mastery(payload.self_ratings, [], 35.0, 1.0, 0.0).mastery
    profile.onboarding_complete = True
    database.commit()
    database.refresh(profile)
    generate_sheet(
        database,
        user.id,
        SheetGenerateRequest(
            goal=payload.goal,
            timeline_days=payload.timeline_days,
            daily_minutes=payload.daily_minutes,
            mastery=profile.mastery,
        ),
    )
    return profile


def update_settings(database: Session, user: User, payload: UserSettingsUpdate) -> UserProfile:
    profile = get_or_create_profile(database, user.id)
    current = dict(profile.settings or {})
    for key, value in payload.model_dump(exclude_none=True).items():
        current[key] = value
    profile.settings = current
    database.commit()
    database.refresh(profile)
    return profile
