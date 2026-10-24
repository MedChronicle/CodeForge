from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from backend.app.api.deps import get_current_admin, get_database
from backend.app.api.routes.serializers import problem_response, resource_response, topic_response
from backend.app.core.exceptions import NotFoundError
from backend.app.models import LearningSheet, Problem, Resource, Topic, User
from backend.app.schemas.admin import AdminStatsResponse
from backend.app.schemas.problem import ProblemCreate, ProblemResponse, ProblemUpdate
from backend.app.schemas.resource import ResourceCreate, ResourceResponse, ResourceUpdate
from backend.app.schemas.topic import TopicCreate, TopicResponse, TopicUpdate


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStatsResponse)
def stats(_: User = Depends(get_current_admin), database: Session = Depends(get_database)) -> AdminStatsResponse:
    return AdminStatsResponse(
        users=database.scalar(select(func.count(User.id))) or 0,
        problems=database.scalar(select(func.count(Problem.id))) or 0,
        topics=database.scalar(select(func.count(Topic.id))) or 0,
        resources=database.scalar(select(func.count(Resource.id))) or 0,
        active_sheets=database.scalar(select(func.count(LearningSheet.id)).where(LearningSheet.is_active.is_(True))) or 0,
    )


@router.post("/topics", response_model=TopicResponse, status_code=201)
def create_topic(payload: TopicCreate, _: User = Depends(get_current_admin), database: Session = Depends(get_database)) -> TopicResponse:
    topic = Topic(**payload.model_dump())
    database.add(topic)
    database.commit()
    database.refresh(topic)
    return topic_response(topic)


@router.patch("/topics/{topic_id}", response_model=TopicResponse)
def update_topic(topic_id: UUID, payload: TopicUpdate, _: User = Depends(get_current_admin), database: Session = Depends(get_database)) -> TopicResponse:
    topic = database.scalar(select(Topic).where(Topic.id == topic_id).options(selectinload(Topic.problems), selectinload(Topic.resources)))
    if topic is None:
        raise NotFoundError("Topic not found")
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(topic, key, value)
    database.commit()
    database.refresh(topic)
    return topic_response(topic)


@router.delete("/topics/{topic_id}")
def delete_topic(topic_id: UUID, _: User = Depends(get_current_admin), database: Session = Depends(get_database)) -> dict[str, str]:
    topic = database.get(Topic, topic_id)
    if topic is None:
        raise NotFoundError("Topic not found")
    topic.is_active = False
    database.commit()
    return {"message": "Topic archived"}


@router.post("/problems", response_model=ProblemResponse, status_code=201)
def create_problem(payload: ProblemCreate, _: User = Depends(get_current_admin), database: Session = Depends(get_database)) -> ProblemResponse:
    problem = Problem(**payload.model_dump())
    database.add(problem)
    database.commit()
    problem = database.scalar(select(Problem).where(Problem.id == problem.id).options(joinedload(Problem.topic)))
    return problem_response(problem)


@router.patch("/problems/{problem_id}", response_model=ProblemResponse)
def update_problem(problem_id: UUID, payload: ProblemUpdate, _: User = Depends(get_current_admin), database: Session = Depends(get_database)) -> ProblemResponse:
    problem = database.scalar(select(Problem).where(Problem.id == problem_id).options(joinedload(Problem.topic)))
    if problem is None:
        raise NotFoundError("Problem not found")
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(problem, key, value)
    database.commit()
    database.refresh(problem)
    return problem_response(problem)


@router.delete("/problems/{problem_id}")
def delete_problem(problem_id: UUID, _: User = Depends(get_current_admin), database: Session = Depends(get_database)) -> dict[str, str]:
    problem = database.get(Problem, problem_id)
    if problem is None:
        raise NotFoundError("Problem not found")
    problem.is_active = False
    database.commit()
    return {"message": "Problem archived"}


@router.post("/resources", response_model=ResourceResponse, status_code=201)
def create_resource(payload: ResourceCreate, _: User = Depends(get_current_admin), database: Session = Depends(get_database)) -> ResourceResponse:
    resource = Resource(**payload.model_dump())
    database.add(resource)
    database.commit()
    resource = database.scalar(select(Resource).where(Resource.id == resource.id).options(joinedload(Resource.topic)))
    return resource_response(resource)


@router.patch("/resources/{resource_id}", response_model=ResourceResponse)
def update_resource(resource_id: UUID, payload: ResourceUpdate, _: User = Depends(get_current_admin), database: Session = Depends(get_database)) -> ResourceResponse:
    resource = database.scalar(select(Resource).where(Resource.id == resource_id).options(joinedload(Resource.topic)))
    if resource is None:
        raise NotFoundError("Resource not found")
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(resource, key, value)
    database.commit()
    database.refresh(resource)
    return resource_response(resource)


@router.delete("/resources/{resource_id}")
def delete_resource(resource_id: UUID, _: User = Depends(get_current_admin), database: Session = Depends(get_database)) -> dict[str, str]:
    resource = database.get(Resource, resource_id)
    if resource is None:
        raise NotFoundError("Resource not found")
    database.delete(resource)
    database.commit()
    return {"message": "Resource deleted"}
