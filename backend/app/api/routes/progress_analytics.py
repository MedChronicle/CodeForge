from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_database
from backend.app.models.user import User
from backend.app.schemas.progress import AnalyticsResponse
from backend.app.services.analytics_service import build_analytics


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard", response_model=AnalyticsResponse)
def dashboard(user: User = Depends(get_current_user), database: Session = Depends(get_database)) -> AnalyticsResponse:
    return AnalyticsResponse(**build_analytics(database, user.id))
