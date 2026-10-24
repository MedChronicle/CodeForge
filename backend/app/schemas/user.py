from pydantic import BaseModel, Field


class UserSettingsUpdate(BaseModel):
    theme: str | None = Field(default=None, pattern=r"^(dark|light|system)$")
    reduce_motion: bool | None = None
    preferred_language: str | None = None
