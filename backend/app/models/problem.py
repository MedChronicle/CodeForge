import uuid

from sqlalchemy import Boolean, Float, ForeignKey, JSON, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, TimestampMixin


class Problem(TimestampMixin, Base):
    __tablename__ = "problems"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"), index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(140), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    companies: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    external_url: Mapped[str] = mapped_column(String(500), nullable=False)
    estimated_minutes: Mapped[int] = mapped_column(nullable=False)
    prerequisites: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    starter_templates: Mapped[dict[str, str]] = mapped_column(JSON, default=dict, nullable=False)
    approach_explanations: Mapped[dict[str, str]] = mapped_column(JSON, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    popularity_score: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)

    topic = relationship("Topic", back_populates="problems")
    progress = relationship("UserProblemProgress", back_populates="problem", cascade="all, delete-orphan")
    sheet_items = relationship("SheetItem", back_populates="problem", cascade="all, delete-orphan")
