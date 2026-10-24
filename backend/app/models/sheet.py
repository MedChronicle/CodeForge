import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, TimestampMixin


class LearningSheet(TimestampMixin, Base):
    __tablename__ = "learning_sheets"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    goal: Mapped[str] = mapped_column(String(40), nullable=False)
    timeline_days: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    starts_on: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    user = relationship("User", back_populates="sheets")
    days = relationship("SheetDay", back_populates="sheet", cascade="all, delete-orphan", order_by="SheetDay.day_number")


class SheetDay(TimestampMixin, Base):
    __tablename__ = "sheet_days"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    sheet_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("learning_sheets.id", ondelete="CASCADE"), index=True, nullable=False)
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    focus_topic: Mapped[str] = mapped_column(String(80), nullable=False)
    estimated_minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    sheet = relationship("LearningSheet", back_populates="days")
    items = relationship("SheetItem", back_populates="day", cascade="all, delete-orphan", order_by="SheetItem.position")


class SheetItem(TimestampMixin, Base):
    __tablename__ = "sheet_items"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    day_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sheet_days.id", ondelete="CASCADE"), index=True, nullable=False)
    problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("problems.id", ondelete="CASCADE"), index=True, nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    day = relationship("SheetDay", back_populates="items")
    problem = relationship("Problem", back_populates="sheet_items")
