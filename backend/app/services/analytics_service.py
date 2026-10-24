from collections import Counter, defaultdict
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from backend.app.models.problem import Problem
from backend.app.models.progress import UserProblemProgress
from backend.app.models.topic import Topic
from backend.app.models.user_profile import UserProfile


def build_analytics(database: Session, user_id: UUID) -> dict:
    progress = list(
        database.scalars(
            select(UserProblemProgress)
            .where(UserProblemProgress.user_id == user_id)
            .options(joinedload(UserProblemProgress.problem).joinedload(Problem.topic))
        ).all()
    )
    profile = database.scalar(select(UserProfile).where(UserProfile.user_id == user_id))
    solved = [item for item in progress if item.status == "solved"]
    topic_counts: dict[str, dict[str, float]] = defaultdict(lambda: {"solved": 0, "total": 0, "mastery": 0.0})
    for item in progress:
        topic = item.problem.topic.name if item.problem and item.problem.topic else "Uncategorized"
        topic_counts[topic]["total"] += 1
        if item.status == "solved":
            topic_counts[topic]["solved"] += 1
            topic_counts[topic]["mastery"] += item.last_score or 1.0
    mastery = [
        {"topic": topic, "mastery": round(values["mastery"] / max(1, values["total"]), 3), "solved": int(values["solved"])}
        for topic, values in topic_counts.items()
    ]
    difficulty = Counter(item.problem.difficulty for item in solved if item.problem)
    activity = Counter(item.solved_at.date().isoformat() for item in solved if item.solved_at)
    recent_activity = []
    for offset in range(13, -1, -1):
        day = (datetime.now(UTC) - timedelta(days=offset)).date().isoformat()
        recent_activity.append({"date": day, "solved": activity.get(day, 0)})
    badges = []
    if len(solved) >= 1:
        badges.append({"name": "First Spark", "description": "Solved your first problem", "unlocked": True})
    if len(solved) >= 10:
        badges.append({"name": "Double Digits", "description": "Solved ten problems", "unlocked": True})
    if profile and profile.current_streak >= 7:
        badges.append({"name": "Seven-Day Signal", "description": "Maintained a seven-day streak", "unlocked": True})
    return {
        "total_problems": database.scalar(select(func.count(Problem.id)).where(Problem.is_active.is_(True))) or 0,
        "solved_problems": len(solved),
        "in_progress_problems": sum(item.status == "in_progress" for item in progress),
        "revisit_problems": sum(item.status == "revisit" for item in progress),
        "xp": profile.xp if profile else 0,
        "level": profile.level if profile else 1,
        "current_streak": profile.current_streak if profile else 0,
        "longest_streak": profile.longest_streak if profile else 0,
        "solved_over_time": recent_activity,
        "mastery_by_topic": mastery,
        "difficulty_distribution": [{"difficulty": key, "count": difficulty.get(key, 0)} for key in ["Easy", "Medium", "Hard"]],
        "recent_activity": [{"title": item.problem.title, "status": item.status, "updated_at": item.updated_at.isoformat()} for item in progress[:8]],
        "badges": badges,
    }
