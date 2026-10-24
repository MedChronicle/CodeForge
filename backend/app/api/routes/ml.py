from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.api.deps import get_current_user, get_database
from backend.app.api.routes.serializers import problem_response
from backend.app.models.problem import Problem
from backend.app.models.progress import UserProblemProgress
from backend.app.models.user import User
from backend.app.models.user_profile import UserProfile
from backend.app.schemas.ml import RecommendationResponse, SkillEstimateRequest, SkillEstimateResponse
from backend.app.schemas.sheet import SheetGenerateRequest, SheetResponse
from backend.app.services.sheet_service import generate_sheet
from backend.app.api.routes.serializers import sheet_response
from backend.ml.recommender import recommend_problems
from backend.ml.skill_estimator import estimate_mastery


router = APIRouter(prefix="/ml", tags=["ml"])


@router.post("/estimate", response_model=SkillEstimateResponse)
def estimate(payload: SkillEstimateRequest) -> SkillEstimateResponse:
    result = estimate_mastery(
        payload.self_ratings,
        payload.solve_history,
        payload.time_per_problem,
        payload.attempts,
        payload.hints_used,
    )
    return SkillEstimateResponse(
        mastery=result.mastery,
        confidence=result.confidence,
        feature_importance=result.feature_importance,
        model_source=result.model_source,
    )


@router.get("/recommend", response_model=list[RecommendationResponse])
def recommend(
    limit: int = 12,
    user: User = Depends(get_current_user),
    database: Session = Depends(get_database),
) -> list[RecommendationResponse]:
    profile = database.scalar(select(UserProfile).where(UserProfile.user_id == user.id))
    mastery = profile.mastery if profile else {}
    progress = database.scalars(select(UserProblemProgress).where(UserProblemProgress.user_id == user.id)).all()
    solved_ids = {str(item.problem_id) for item in progress if item.status == "solved"}
    due_ids = {str(item.problem_id) for item in progress if item.next_review_at is not None}
    problems = database.scalars(select(Problem).where(Problem.is_active.is_(True)).options(joinedload(Problem.topic))).all()
    ranked = recommend_problems(
        [
            {
                "id": problem.id,
                "title": problem.title,
                "topic": problem.topic.slug if problem.topic else "arrays",
                "difficulty": problem.difficulty,
                "popularity_score": problem.popularity_score,
            }
            for problem in problems
        ],
        mastery,
        solved_ids,
        due_ids,
        min(30, max(1, limit)),
    )
    return [
        RecommendationResponse(
            problem_id=str(item["id"]),
            title=item["title"],
            topic=item["topic"],
            difficulty=item["difficulty"],
            score=item["score"],
            reason=item["reason"],
        )
        for item in ranked
    ]
