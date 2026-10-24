from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from backend.app.core.exceptions import DomainError, NotFoundError
from backend.app.models.problem import Problem
from backend.app.models.sheet import LearningSheet, SheetDay, SheetItem
from backend.app.models.topic import Topic
from backend.app.schemas.sheet import SheetGenerateRequest
from backend.ml.sheet_generator import generate_day_plan


def build_problem_dict(problem: Problem) -> dict:
    return {
        "id": str(problem.id),
        "topic": problem.topic.slug if problem.topic else "unknown",
        "topic_name": problem.topic.name if problem.topic else "Unknown",
        "title": problem.title,
        "difficulty": problem.difficulty,
        "estimated_minutes": problem.estimated_minutes,
        "prerequisites": problem.prerequisites,
    }


def generate_sheet(database: Session, user_id: UUID, payload: SheetGenerateRequest) -> LearningSheet:
    topics = list(database.scalars(select(Topic).where(Topic.is_active.is_(True)).order_by(Topic.order_index)).all())
    problems = list(
        database.scalars(
            select(Problem)
            .where(Problem.is_active.is_(True))
            .options(joinedload(Problem.topic))
            .order_by(Problem.popularity_score.desc())
        ).all()
    )
    if not topics or not problems:
        raise DomainError("Seed topics and problems before generating a sheet", 409)
    plan = generate_day_plan(
        topics=[
            {"slug": topic.slug, "name": topic.name, "prerequisites": topic.prerequisites, "order_index": topic.order_index}
            for topic in topics
        ],
        problems=[build_problem_dict(problem) for problem in problems],
        goal=payload.goal,
        timeline_days=payload.timeline_days,
        daily_minutes=payload.daily_minutes,
        mastery=payload.mastery,
    )
    old_sheets = database.scalars(select(LearningSheet).where(LearningSheet.user_id == user_id, LearningSheet.is_active.is_(True))).all()
    for old in old_sheets:
        old.is_active = False
    sheet = LearningSheet(
        user_id=user_id,
        title=f"{payload.timeline_days}-Day {payload.goal.replace('_', ' ').title()} Forge",
        goal=payload.goal,
        timeline_days=payload.timeline_days,
        daily_minutes=payload.daily_minutes,
        starts_on=date.today(),
    )
    database.add(sheet)
    database.flush()
    by_id = {str(problem.id): problem for problem in problems}
    for day_data in plan:
        day = SheetDay(
            sheet_id=sheet.id,
            day_number=day_data["day_number"],
            date=date.today() + timedelta(days=day_data["day_number"] - 1),
            focus_topic=day_data["focus_topic"],
            estimated_minutes=day_data["estimated_minutes"],
        )
        database.add(day)
        database.flush()
        for position, problem_id in enumerate(day_data["problem_ids"], start=1):
            if problem_id in by_id:
                database.add(SheetItem(day_id=day.id, problem_id=by_id[problem_id].id, position=position))
    database.commit()
    database.refresh(sheet)
    return sheet


def get_active_sheet(database: Session, user_id: UUID) -> LearningSheet:
    sheet = database.scalar(
        select(LearningSheet)
        .where(LearningSheet.user_id == user_id, LearningSheet.is_active.is_(True))
        .options(
            selectinload(LearningSheet.days)
            .selectinload(SheetDay.items)
            .joinedload(SheetItem.problem)
            .joinedload(Problem.topic)
        )
        .order_by(LearningSheet.created_at.desc())
    )
    if sheet is None:
        raise NotFoundError("No active learning sheet. Complete onboarding first.")
    return sheet
