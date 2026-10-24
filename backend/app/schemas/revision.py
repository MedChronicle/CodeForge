from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from backend.app.schemas.problem import ProblemResponse


class ReviewRequest(BaseModel):
    quality: int = Field(ge=0, le=5)


class RevisionItemResponse(BaseModel):
    progress_id: UUID
    problem: ProblemResponse
    due_at: datetime
    interval_days: int
    repetition: int
