from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_database
from backend.app.api.routes.serializers import sheet_response
from backend.app.models.user import User
from backend.app.schemas.sheet import SheetGenerateRequest, SheetResponse
from backend.app.services.sheet_service import generate_sheet, get_active_sheet


router = APIRouter(prefix="/sheet", tags=["sheet"])


@router.get("/active", response_model=SheetResponse)
def active_sheet(user: User = Depends(get_current_user), database: Session = Depends(get_database)) -> SheetResponse:
    return sheet_response(get_active_sheet(database, user.id))


@router.post("/generate", response_model=SheetResponse)
def create_sheet(
    payload: SheetGenerateRequest,
    user: User = Depends(get_current_user),
    database: Session = Depends(get_database),
) -> SheetResponse:
    return sheet_response(generate_sheet(database, user.id, payload))
