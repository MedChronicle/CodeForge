from pydantic import BaseModel, Field, field_validator


SUPPORTED_LANGUAGES = {"cpp", "java", "python", "javascript", "go", "csharp", "kotlin"}
SUPPORTED_GOALS = {"placements", "faang", "competitive_programming", "college_exams"}
SUPPORTED_EXPERIENCE = {"beginner", "intermediate", "advanced"}


class OnboardingRequest(BaseModel):
    experience_level: str = Field(min_length=3, max_length=30)
    # A learner may honestly rate every topic as "not started". An empty map
    # is therefore valid and is converted into cold-start estimates by ML.
    self_ratings: dict[str, float] = Field(default_factory=dict)
    preferred_languages: list[str] = Field(min_length=1, max_length=7)
    goal: str = Field(min_length=3, max_length=40)
    timeline_days: int = Field(ge=30, le=365)
    daily_minutes: int = Field(ge=15, le=480)

    @field_validator("experience_level")
    @classmethod
    def valid_experience(cls, value: str) -> str:
        if value not in SUPPORTED_EXPERIENCE:
            raise ValueError(f"Experience must be one of {sorted(SUPPORTED_EXPERIENCE)}")
        return value

    @field_validator("goal")
    @classmethod
    def valid_goal(cls, value: str) -> str:
        if value not in SUPPORTED_GOALS:
            raise ValueError(f"Goal must be one of {sorted(SUPPORTED_GOALS)}")
        return value

    @field_validator("preferred_languages")
    @classmethod
    def valid_languages(cls, values: list[str]) -> list[str]:
        normalized = list(dict.fromkeys(values))
        unknown = set(normalized) - SUPPORTED_LANGUAGES
        if unknown:
            raise ValueError(f"Unsupported languages: {sorted(unknown)}")
        return normalized

    @field_validator("self_ratings")
    @classmethod
    def valid_ratings(cls, values: dict[str, float]) -> dict[str, float]:
        if any(not 0 <= score <= 5 for score in values.values()):
            raise ValueError("Self-ratings must be between 0 and 5")
        return {key.strip().lower(): round(float(value), 2) for key, value in values.items() if key.strip()}


class ProfileResponse(BaseModel):
    experience_level: str
    self_ratings: dict[str, float]
    preferred_languages: list[str]
    goal: str
    timeline_days: int
    daily_minutes: int
    mastery: dict[str, float]
    xp: int
    level: int
    current_streak: int
    longest_streak: int
    onboarding_complete: bool
