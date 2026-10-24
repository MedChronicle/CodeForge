from uuid import UUID

from pydantic import BaseModel, Field

from backend.app.schemas.common import ORMModel


class TopicBase(BaseModel):
    slug: str = Field(min_length=2, max_length=80, pattern=r"^[a-z0-9-]+$")
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=10, max_length=500)
    order_index: int = Field(ge=0)
    prerequisites: list[str] = Field(default_factory=list)
    notes_markdown: str = ""
    color: str = Field(default="#8b5cf6", min_length=4, max_length=20)


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, min_length=10, max_length=500)
    order_index: int | None = Field(default=None, ge=0)
    prerequisites: list[str] | None = None
    notes_markdown: str | None = None
    color: str | None = Field(default=None, min_length=4, max_length=20)
    is_active: bool | None = None


class TopicResponse(ORMModel):
    id: UUID
    slug: str
    name: str
    description: str
    order_index: int
    prerequisites: list[str]
    notes_markdown: str
    color: str
    problem_count: int = 0
    resource_count: int = 0
