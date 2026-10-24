from backend.app.core.security import decode_token, hash_password, verify_password
from backend.app.schemas.auth import LoginRequest, RegisterRequest
from backend.app.schemas.onboarding import OnboardingRequest
from backend.app.services.auth_service import authenticate_user, issue_tokens, register_user


def test_password_hash_round_trip() -> None:
    password_hash = hash_password("correct-horse-42")
    assert password_hash != "correct-horse-42"
    assert verify_password("correct-horse-42", password_hash)
    assert not verify_password("wrong-password", password_hash)


def test_register_authenticate_and_issue_tokens(database) -> None:
    payload = RegisterRequest(email="learner@example.com", password="secret123", display_name="Learner")
    user = register_user(database, payload)
    authenticated = authenticate_user(database, LoginRequest(email=payload.email, password=payload.password))
    access, refresh = issue_tokens(database, authenticated)
    assert user.id == authenticated.id
    assert decode_token(access)["sub"] == str(user.id)
    assert decode_token(refresh, expected_type="refresh")["sub"] == str(user.id)


def test_onboarding_accepts_a_zero_signal_cold_start() -> None:
    payload = OnboardingRequest(
        experience_level="beginner",
        self_ratings={},
        preferred_languages=["python"],
        goal="placements",
        timeline_days=90,
        daily_minutes=60,
    )
    assert payload.self_ratings == {}
