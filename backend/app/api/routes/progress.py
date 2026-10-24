from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_database
from backend.app.models.progress import UserProblemProgress
from backend.app.models.user import User
from backend.app.schemas.progress import ProgressResponse, ProgressUpdate
from backend.app.services.progress_service import list_user_progress, update_progress


router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=list[ProgressResponse])
def progress_list(user: User = Depends(get_current_user), database: Session = Depends(get_database)) -> list[ProgressResponse]:
    return [ProgressResponse.model_validate(item) for item in list_user_progress(database, user.id)]


@router.put("/{problem_id}", response_model=ProgressResponse)
def update_problem_progress(
    problem_id: UUID,
    payload: ProgressUpdate,
    user: User = Depends(get_current_user),
    database: Session = Depends(get_database),
) -> ProgressResponse:
    return ProgressResponse.model_validate(update_progress(database, user, problem_id, payload))
