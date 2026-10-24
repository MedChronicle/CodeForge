from pydantic import BaseModel, Field


class SkillEstimateRequest(BaseModel):
    self_ratings: dict[str, float] = Field(default_factory=dict)
    solve_history: list[dict] = Field(default_factory=list)
    time_per_problem: float = Field(default=35.0, ge=1, le=1000)
    attempts: float = Field(default=1.0, ge=0, le=1000)
    hints_used: float = Field(default=0.0, ge=0, le=1000)


class SkillEstimateResponse(BaseModel):
    mastery: dict[str, float]
    confidence: dict[str, float]
    feature_importance: dict[str, float]
    model_source: str


class RecommendationResponse(BaseModel):
    problem_id: str
    title: str
    topic: str
    difficulty: str
    score: float
    reason: str
