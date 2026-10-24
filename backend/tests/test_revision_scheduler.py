from datetime import UTC, datetime
from uuid import uuid4

from backend.app.models.progress import UserProblemProgress
from backend.app.services.revision_service import calculate_sm2


def test_successful_sm2_reviews_expand_interval() -> None:
    progress = UserProblemProgress(user_id=uuid4(), problem_id=uuid4())
    ease, first_interval, first_repetition = calculate_sm2(progress, 5)
    progress.ease_factor = ease
    progress.interval_days = first_interval
    progress.repetition = first_repetition
    ease, second_interval, second_repetition = calculate_sm2(progress, 5)
    assert first_interval == 1
    assert second_interval == 6
    assert second_repetition == 2
    assert ease >= 2.5


def test_low_quality_review_resets_repetition() -> None:
    progress = UserProblemProgress(
        user_id=uuid4(),
        problem_id=uuid4(),
        ease_factor=2.4,
        interval_days=12,
        repetition=4,
        next_review_at=datetime.now(UTC),
    )
    ease, interval, repetition = calculate_sm2(progress, 1)
    assert ease >= 1.3
    assert interval == 1
    assert repetition == 0
