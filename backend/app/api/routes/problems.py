from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.api.deps import get_database, get_optional_user
from backend.app.api.routes.serializers import problem_response
from backend.app.models.problem import Problem
from backend.app.models.progress import UserProblemProgress
from backend.app.models.user import User
from backend.app.schemas.common import PaginatedResponse, Pagination
from backend.app.schemas.problem import ProblemResponse


router = APIRouter(prefix="/problems", tags=["problems"])


@router.get("", response_model=PaginatedResponse[ProblemResponse])
def list_problems(
    topic: str | None = None,
    difficulty: str | None = None,
    company: str | None = None,
    status: str | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 30,
    user: User | None = Depends(get_optional_user),
    database: Session = Depends(get_database),
) -> PaginatedResponse[ProblemResponse]:
    page = max(1, page)
    page_size = max(1, min(100, page_size))
    query = select(Problem).where(Problem.is_active.is_(True)).options(joinedload(Problem.topic))
    if topic:
        query = query.where(Problem.topic.has(slug=topic))
    if difficulty:
        query = query.where(Problem.difficulty == difficulty)
    if company:
        query = query.where(Problem.companies.contains([company]))
    if search:
        query = query.where(Problem.title.ilike(f"%{search.strip()}%"))
    problems = list(database.scalars(query.order_by(Problem.topic_id, Problem.difficulty, Problem.title)).all())
    if status:
        if user is None:
            return PaginatedResponse(items=[], pagination=Pagination(page=page, page_size=page_size, total=0))
        progress_rows = database.scalars(
            select(UserProblemProgress).where(UserProblemProgress.user_id == user.id, UserProblemProgress.status == status)
        ).all()
        allowed = {row.problem_id for row in progress_rows}
        problems = [problem for problem in problems if problem.id in allowed]
    total = len(problems)
    start = (page - 1) * page_size
    items = [problem_response(problem) for problem in problems[start : start + page_size]]
    return PaginatedResponse(items=items, pagination=Pagination(page=page, page_size=page_size, total=total))


@router.get("/{problem_id}", response_model=ProblemResponse)
def get_problem(problem_id: UUID, database: Session = Depends(get_database)) -> ProblemResponse:
    problem = database.scalar(select(Problem).where(Problem.id == problem_id, Problem.is_active.is_(True)).options(joinedload(Problem.topic)))
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem_response(problem)
