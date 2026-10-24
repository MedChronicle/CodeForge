from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.api.deps import get_database
from backend.app.api.routes.serializers import resource_response
from backend.app.models.resource import Resource
from backend.app.schemas.resource import ResourceResponse


router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("", response_model=list[ResourceResponse])
def list_resources(topic: str | None = None, kind: str | None = None, database: Session = Depends(get_database)) -> list[ResourceResponse]:
    query = select(Resource).options(joinedload(Resource.topic)).order_by(Resource.created_at)
    if topic:
        query = query.where(Resource.topic.has(slug=topic))
    if kind:
        query = query.where(Resource.kind == kind)
    return [resource_response(resource) for resource in database.scalars(query).all()]
