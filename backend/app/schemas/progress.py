from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from backend.app.schemas.common import ORMModel


class ProgressUpdate(BaseModel):
    status: str = Field(pattern=r"^(todo|in_progress|solved|revisit)$")
    notes: str = Field(default="", max_length=4000)
    bookmarked: bool = False
    attempts: int = Field(default=0, ge=0, le=1000)
    hints_used: int = Field(default=0, ge=0, le=100)
    total_time_seconds: int = Field(default=0, ge=0, le=86400)
    score: float = Field(default=0.0, ge=0, le=1)


class ProgressResponse(ORMModel):
    id: UUID
    problem_id: UUID
    status: str
    notes: str
    bookmarked: bool
    attempts: int
    hints_used: int
    total_time_seconds: int
    last_score: float
    solved_at: datetime | None
    next_review_at: datetime | None
    interval_days: int
    repetition: int


class AnalyticsResponse(BaseModel):
    total_problems: int
    solved_problems: int
    in_progress_problems: int
    revisit_problems: int
    xp: int
    level: int
    current_streak: int
    longest_streak: int
    solved_over_time: list[dict]
    mastery_by_topic: list[dict]
    difficulty_distribution: list[dict]
    recent_activity: list[dict]
    badges: list[dict]
