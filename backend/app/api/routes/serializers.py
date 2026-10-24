from backend.app.models.problem import Problem
from backend.app.models.resource import Resource
from backend.app.models.sheet import LearningSheet
from backend.app.models.topic import Topic
from backend.app.schemas.problem import ProblemResponse
from backend.app.schemas.resource import ResourceResponse
from backend.app.schemas.sheet import SheetResponse
from backend.app.schemas.topic import TopicResponse


def problem_response(problem: Problem, status: str | None = None) -> ProblemResponse:
    return ProblemResponse(
        id=problem.id,
        topic_id=problem.topic_id,
        topic_slug=problem.topic.slug if problem.topic else None,
        topic_name=problem.topic.name if problem.topic else None,
        slug=problem.slug,
        title=problem.title,
        difficulty=problem.difficulty,
        tags=problem.tags,
        companies=problem.companies,
        external_url=problem.external_url,
        estimated_minutes=problem.estimated_minutes,
        prerequisites=problem.prerequisites,
        starter_templates=problem.starter_templates,
        approach_explanations=problem.approach_explanations,
        popularity_score=problem.popularity_score,
    )


def topic_response(topic: Topic) -> TopicResponse:
    return TopicResponse(
        id=topic.id,
        slug=topic.slug,
        name=topic.name,
        description=topic.description,
        order_index=topic.order_index,
        prerequisites=topic.prerequisites,
        notes_markdown=topic.notes_markdown,
        color=topic.color,
        problem_count=len(topic.problems) if topic.problems is not None else 0,
        resource_count=len(topic.resources) if topic.resources is not None else 0,
    )


def resource_response(resource: Resource) -> ResourceResponse:
    return ResourceResponse(
        id=resource.id,
        topic_id=resource.topic_id,
        topic_name=resource.topic.name if resource.topic else None,
        title=resource.title,
        channel=resource.channel,
        url=resource.url,
        kind=resource.kind,
        description=resource.description,
    )


def sheet_response(sheet: LearningSheet) -> SheetResponse:
    return SheetResponse(
        id=sheet.id,
        title=sheet.title,
        goal=sheet.goal,
        timeline_days=sheet.timeline_days,
        daily_minutes=sheet.daily_minutes,
        starts_on=sheet.starts_on,
        days=[
            {
                "id": day.id,
                "day_number": day.day_number,
                "date": day.date,
                "focus_topic": day.focus_topic,
                "estimated_minutes": day.estimated_minutes,
                "items": [
                    {"id": item.id, "position": item.position, "problem": problem_response(item.problem)}
                    for item in day.items
                ],
            }
            for day in sheet.days
        ],
    )
