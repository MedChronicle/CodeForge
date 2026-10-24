import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, TimestampMixin


class UserProblemProgress(TimestampMixin, Base):
    __tablename__ = "user_problem_progress"
    __table_args__ = (UniqueConstraint("user_id", "problem_id", name="uq_user_problem_progress"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("problems.id", ondelete="CASCADE"), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="todo", nullable=False)
    notes: Mapped[str] = mapped_column(String(4000), default="", nullable=False)
    bookmarked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    hints_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_time_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    solved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ease_factor: Mapped[float] = mapped_column(Float, default=2.5, nullable=False)
    interval_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    repetition: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    next_review_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    review_history: Mapped[list[dict]] = mapped_column(JSON, default=list, nullable=False)

    user = relationship("User", back_populates="progress")
    problem = relationship("Problem", back_populates="progress")

    def mark_solved(self, score: float = 1.0) -> None:
        self.status = "solved"
        self.last_score = max(0.0, min(1.0, score))
        self.solved_at = datetime.now(UTC)
