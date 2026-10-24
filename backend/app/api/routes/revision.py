from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_database
from backend.app.api.routes.serializers import problem_response
from backend.app.models.user import User
from backend.app.schemas.revision import RevisionItemResponse, ReviewRequest
from backend.app.services.revision_service import due_revisions, review_progress


router = APIRouter(prefix="/revision", tags=["revision"])


@router.get("/today", response_model=list[RevisionItemResponse])
def today_queue(user: User = Depends(get_current_user), database: Session = Depends(get_database)) -> list[RevisionItemResponse]:
    return [
        RevisionItemResponse(
            progress_id=item.id,
            problem=problem_response(item.problem),
            due_at=item.next_review_at,
            interval_days=item.interval_days,
            repetition=item.repetition,
        )
        for item in due_revisions(database, user.id)
    ]


@router.post("/{progress_id}/review", response_model=RevisionItemResponse)
def review(
    progress_id: UUID,
    payload: ReviewRequest,
    user: User = Depends(get_current_user),
    database: Session = Depends(get_database),
) -> RevisionItemResponse:
    item = review_progress(database, user.id, progress_id, payload)
    return RevisionItemResponse(
        progress_id=item.id,
        problem=problem_response(item.problem),
        due_at=item.next_review_at,
        interval_days=item.interval_days,
        repetition=item.repetition,
    )
