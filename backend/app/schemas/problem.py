from uuid import UUID

from pydantic import BaseModel, Field

from backend.app.schemas.common import ORMModel


class ProblemBase(BaseModel):
    topic_id: UUID
    slug: str = Field(min_length=2, max_length=140, pattern=r"^[a-z0-9-]+$")
    title: str = Field(min_length=2, max_length=180)
    difficulty: str = Field(pattern=r"^(Easy|Medium|Hard)$")
    tags: list[str] = Field(default_factory=list, max_length=20)
    companies: list[str] = Field(default_factory=list, max_length=20)
    external_url: str = Field(min_length=10, max_length=500)
    estimated_minutes: int = Field(ge=5, le=240)
    prerequisites: list[str] = Field(default_factory=list)
    starter_templates: dict[str, str] = Field(default_factory=dict)
    approach_explanations: dict[str, str] = Field(default_factory=dict)
    popularity_score: float = Field(default=0.5, ge=0, le=1)


class ProblemCreate(ProblemBase):
    pass


class ProblemUpdate(BaseModel):
    topic_id: UUID | None = None
    title: str | None = Field(default=None, min_length=2, max_length=180)
    difficulty: str | None = Field(default=None, pattern=r"^(Easy|Medium|Hard)$")
    tags: list[str] | None = None
    companies: list[str] | None = None
    external_url: str | None = Field(default=None, min_length=10, max_length=500)
    estimated_minutes: int | None = Field(default=None, ge=5, le=240)
    prerequisites: list[str] | None = None
    starter_templates: dict[str, str] | None = None
    approach_explanations: dict[str, str] | None = None
    popularity_score: float | None = Field(default=None, ge=0, le=1)
    is_active: bool | None = None


class ProblemResponse(ORMModel):
    id: UUID
    topic_id: UUID
    topic_slug: str | None = None
    topic_name: str | None = None
    slug: str
    title: str
    difficulty: str
    tags: list[str]
    companies: list[str]
    external_url: str
    estimated_minutes: int
    prerequisites: list[str]
    starter_templates: dict[str, str]
    approach_explanations: dict[str, str]
    popularity_score: float


class ProblemFilters(BaseModel):
    topic: str | None = None
    difficulty: str | None = None
    company: str | None = None
    status: str | None = None
    search: str | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=30, ge=1, le=100)
