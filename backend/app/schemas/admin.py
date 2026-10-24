from pydantic import BaseModel


class AdminStatsResponse(BaseModel):
    users: int
    problems: int
    topics: int
    resources: int
    active_sheets: int
