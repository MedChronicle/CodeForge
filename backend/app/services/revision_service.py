from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.core.exceptions import NotFoundError
from backend.app.models.problem import Problem
from backend.app.models.progress import UserProblemProgress
from backend.app.schemas.revision import ReviewRequest


def calculate_sm2(progress: UserProblemProgress, quality: int) -> tuple[float, int, int]:
    """Return updated ease factor, interval, and repetition using SM-2.

    The first two successful reviews use one and six days, then the interval
    grows by the ease factor. Low-quality reviews reset the repetition count.
    """
    quality = max(0, min(5, quality))
    current_ease = progress.ease_factor if progress.ease_factor is not None else 2.5
    current_interval = progress.interval_days if progress.interval_days is not None else 0
    current_repetition = progress.repetition if progress.repetition is not None else 0
    ease = current_ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ease = max(1.3, ease)
    if quality < 3:
        return ease, 1, 0
    repetition = current_repetition + 1
    if repetition == 1:
        interval = 1
    elif repetition == 2:
        interval = 6
    else:
        interval = max(1, round(current_interval * ease))
    return ease, interval, repetition


def review_progress(database: Session, user_id: UUID, progress_id: UUID, payload: ReviewRequest) -> UserProblemProgress:
    progress = database.scalar(
        select(UserProblemProgress).where(
            UserProblemProgress.id == progress_id,
            UserProblemProgress.user_id == user_id,
        )
    )
    if progress is None:
        raise NotFoundError("Revision item not found")
    ease, interval, repetition = calculate_sm2(progress, payload.quality)
    progress.ease_factor = ease
    progress.interval_days = interval
    progress.repetition = repetition
    progress.next_review_at = datetime.now(UTC) + timedelta(days=interval)
    progress.review_history = [
        *progress.review_history,
        {"quality": payload.quality, "reviewed_at": datetime.now(UTC).isoformat(), "interval_days": interval},
    ][-30:]
    database.commit()
    database.refresh(progress)
    return progress


def due_revisions(database: Session, user_id: UUID, limit: int = 20) -> list[UserProblemProgress]:
    now = datetime.now(UTC)
    return list(
        database.scalars(
            select(UserProblemProgress)
            .where(
                UserProblemProgress.user_id == user_id,
                UserProblemProgress.status == "solved",
                UserProblemProgress.next_review_at.is_not(None),
                UserProblemProgress.next_review_at <= now,
            )
            .options(joinedload(UserProblemProgress.problem).joinedload(Problem.topic))
            .order_by(UserProblemProgress.next_review_at.asc())
            .limit(limit)
        ).all()
    )
