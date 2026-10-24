from datetime import UTC, date, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.core.exceptions import NotFoundError
from backend.app.models.problem import Problem
from backend.app.models.progress import UserProblemProgress
from backend.app.models.topic import Topic
from backend.app.models.user import User
from backend.app.models.user_profile import UserProfile
from backend.app.schemas.progress import ProgressUpdate


def get_or_create_progress(database: Session, user_id: UUID, problem_id: UUID) -> UserProblemProgress:
    progress = database.scalar(
        select(UserProblemProgress).where(
            UserProblemProgress.user_id == user_id,
            UserProblemProgress.problem_id == problem_id,
        )
    )
    if progress is None:
        if database.scalar(select(Problem.id).where(Problem.id == problem_id)) is None:
            raise NotFoundError("Problem not found")
        progress = UserProblemProgress(user_id=user_id, problem_id=problem_id)
        database.add(progress)
        database.flush()
    return progress


def update_progress(database: Session, user: User, problem_id: UUID, payload: ProgressUpdate) -> UserProblemProgress:
    progress = get_or_create_progress(database, user.id, problem_id)
    was_solved = progress.status == "solved"
    progress.status = payload.status
    progress.notes = payload.notes.strip()
    progress.bookmarked = payload.bookmarked
    progress.attempts = payload.attempts
    progress.hints_used = payload.hints_used
    progress.total_time_seconds = payload.total_time_seconds
    progress.last_score = payload.score
    if payload.status == "solved" and not was_solved:
        progress.solved_at = datetime.now(UTC)
        progress.next_review_at = datetime.now(UTC)
        update_streak_and_xp(database, user, xp_delta=problem_xp(database, problem_id))
    elif payload.status == "solved" and progress.solved_at is None:
        progress.solved_at = datetime.now(UTC)
    database.commit()
    database.refresh(progress)
    return progress


def problem_xp(database: Session, problem_id: UUID) -> int:
    difficulty = database.scalar(select(Problem.difficulty).where(Problem.id == problem_id))
    return {"Easy": 20, "Medium": 40, "Hard": 70}.get(difficulty or "Easy", 20)


def update_streak_and_xp(database: Session, user: User, xp_delta: int) -> None:
    profile = database.scalar(select(UserProfile).where(UserProfile.user_id == user.id))
    if profile is None:
        profile = UserProfile(user_id=user.id)
        database.add(profile)
        database.flush()
    today = date.today().isoformat()
    if profile.last_activity_date != today:
        profile.current_streak = profile.current_streak + 1 if profile.last_activity_date else 1
        profile.longest_streak = max(profile.longest_streak, profile.current_streak)
        profile.last_activity_date = today
    profile.xp += xp_delta
    profile.level = max(1, profile.xp // 500 + 1)


def list_user_progress(database: Session, user_id: UUID) -> list[UserProblemProgress]:
    return list(
        database.scalars(
            select(UserProblemProgress)
            .where(UserProblemProgress.user_id == user_id)
            .options(joinedload(UserProblemProgress.problem).joinedload(Problem.topic))
            .order_by(UserProblemProgress.updated_at.desc())
        ).all()
    )
