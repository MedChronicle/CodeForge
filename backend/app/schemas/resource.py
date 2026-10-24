from uuid import UUID

from pydantic import BaseModel, Field

from backend.app.schemas.common import ORMModel


class ResourceBase(BaseModel):
    topic_id: UUID
    title: str = Field(min_length=2, max_length=180)
    channel: str = Field(min_length=2, max_length=120)
    url: str = Field(min_length=10, max_length=500)
    kind: str = Field(default="video", min_length=2, max_length=30)
    description: str = Field(default="", max_length=1000)


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    topic_id: UUID | None = None
    title: str | None = Field(default=None, min_length=2, max_length=180)
    channel: str | None = Field(default=None, min_length=2, max_length=120)
    url: str | None = Field(default=None, min_length=10, max_length=500)
    kind: str | None = Field(default=None, min_length=2, max_length=30)
    description: str | None = Field(default=None, max_length=1000)


class ResourceResponse(ORMModel):
    id: UUID
    topic_id: UUID
    topic_name: str | None = None
    title: str
    channel: str
    url: str
    kind: str
    description: str
