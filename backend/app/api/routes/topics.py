from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from backend.app.api.deps import get_database
from backend.app.api.routes.serializers import topic_response
from backend.app.models.topic import Topic
from backend.app.schemas.topic import TopicResponse


router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("", response_model=list[TopicResponse])
def list_topics(database: Session = Depends(get_database)) -> list[TopicResponse]:
    topics = database.scalars(
        select(Topic).where(Topic.is_active.is_(True)).options(selectinload(Topic.problems), selectinload(Topic.resources)).order_by(Topic.order_index)
    ).all()
    return [topic_response(topic) for topic in topics]


@router.get("/{slug}", response_model=TopicResponse)
def get_topic(slug: str, database: Session = Depends(get_database)) -> TopicResponse:
    topic = database.scalar(
        select(Topic).where(Topic.slug == slug, Topic.is_active.is_(True)).options(selectinload(Topic.problems), selectinload(Topic.resources))
    )
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic_response(topic)
