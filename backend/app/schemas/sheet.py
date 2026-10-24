from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from backend.app.schemas.problem import ProblemResponse


class SheetGenerateRequest(BaseModel):
    goal: str = Field(min_length=3, max_length=40)
    timeline_days: int = Field(ge=30, le=365)
    daily_minutes: int = Field(ge=15, le=480)
    mastery: dict[str, float] = Field(default_factory=dict)


class SheetItemResponse(BaseModel):
    id: UUID
    position: int
    problem: ProblemResponse


class SheetDayResponse(BaseModel):
    id: UUID
    day_number: int
    date: date
    focus_topic: str
    estimated_minutes: int
    items: list[SheetItemResponse]


class SheetResponse(BaseModel):
    id: UUID
    title: str
    goal: str
    timeline_days: int
    daily_minutes: int
    starts_on: date
    days: list[SheetDayResponse]
