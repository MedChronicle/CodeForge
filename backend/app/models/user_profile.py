import uuid
from typing import Any

from sqlalchemy import JSON, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, TimestampMixin


class UserProfile(TimestampMixin, Base):
    __tablename__ = "user_profiles"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    experience_level: Mapped[str] = mapped_column(String(30), default="beginner", nullable=False)
    goal: Mapped[str] = mapped_column(String(40), default="placements", nullable=False)
    timeline_days: Mapped[int] = mapped_column(Integer, default=90, nullable=False)
    daily_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    preferred_languages: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    self_ratings: Mapped[dict[str, float]] = mapped_column(JSON, default=dict, nullable=False)
    mastery: Mapped[dict[str, float]] = mapped_column(JSON, default=dict, nullable=False)
    xp: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    current_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_activity_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    onboarding_complete: Mapped[bool] = mapped_column(default=False, nullable=False)
    settings: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)

    user = relationship("User", back_populates="profile")
