from __future__ import annotations

from collections import defaultdict


def topological_topics(topics: list[dict]) -> list[dict]:
    """Stable topological sort that falls back to catalog order for cycles."""
    by_slug = {topic["slug"]: topic for topic in topics}
    visited: set[str] = set()
    visiting: set[str] = set()
    ordered: list[dict] = []

    def visit(slug: str) -> None:
        if slug in visited:
            return
        if slug in visiting:
            return
        visiting.add(slug)
        topic = by_slug[slug]
        for prerequisite in topic.get("prerequisites", []):
            if prerequisite in by_slug:
                visit(prerequisite)
        visiting.remove(slug)
        visited.add(slug)
        ordered.append(topic)

    for topic in sorted(topics, key=lambda item: item.get("order_index", 0)):
        visit(topic["slug"])
    return ordered


def _difficulty_rank(difficulty: str) -> int:
    return {"Easy": 1, "Medium": 2, "Hard": 3}.get(difficulty, 1)


def generate_day_plan(
    topics: list[dict],
    problems: list[dict],
    goal: str,
    timeline_days: int,
    daily_minutes: int,
    mastery: dict[str, float],
) -> list[dict]:
    """Create a bounded day-by-day plan without duplicating a problem.

    The planner prioritizes weaker topics but keeps prerequisites ahead of their
    dependants. It leaves the final days lighter when the catalog is exhausted.
    """
    ordered_topics = topological_topics(topics)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for problem in problems:
        grouped[problem["topic"]].append(problem)
    for topic_problems in grouped.values():
        topic_problems.sort(key=lambda item: (_difficulty_rank(item.get("difficulty", "Easy")), item.get("title", "")))
    topic_order = sorted(
        ordered_topics,
        key=lambda topic: (float(mastery.get(topic["slug"], 0.35)), topic.get("order_index", 0)),
    )
    if goal == "competitive_programming":
        topic_order = sorted(topic_order, key=lambda topic: (topic.get("slug") not in {"graphs", "dynamic-programming", "math"}, topic.get("order_index", 0)))
    cursor = {topic["slug"]: 0 for topic in ordered_topics}
    plan: list[dict] = []
    for day_number in range(1, timeline_days + 1):
        if not any(cursor[topic["slug"]] < len(grouped[topic["slug"]]) for topic in ordered_topics):
            break
        candidates = [topic for topic in topic_order if cursor[topic["slug"]] < len(grouped[topic["slug"]])]
        focus = candidates[(day_number - 1) % len(candidates)]
        selected: list[str] = []
        minutes = 0
        for topic in [focus, *candidates]:
            if topic["slug"] != focus["slug"] and selected:
                break
            bucket = grouped[topic["slug"]]
            while cursor[topic["slug"]] < len(bucket):
                problem = bucket[cursor[topic["slug"]]]
                if minutes + problem.get("estimated_minutes", 30) > daily_minutes and selected:
                    break
                selected.append(str(problem["id"]))
                minutes += problem.get("estimated_minutes", 30)
                cursor[topic["slug"]] += 1
                if len(selected) >= 4:
                    break
            if selected:
                break
        plan.append(
            {
                "day_number": day_number,
                "focus_topic": focus["name"],
                "estimated_minutes": min(minutes, daily_minutes),
                "problem_ids": selected,
            }
        )
    return plan
