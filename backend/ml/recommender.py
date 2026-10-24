from __future__ import annotations

from datetime import UTC, datetime


DIFFICULTY_VALUE = {"Easy": 0.25, "Medium": 0.55, "Hard": 0.8}


def recommend_problems(
    problems: list[dict],
    mastery: dict[str, float],
    solved_ids: set[str] | None = None,
    due_ids: set[str] | None = None,
    limit: int = 12,
) -> list[dict]:
    """Rank content by weak-topic relevance, ZPD difficulty, and revision due-ness."""
    solved_ids = solved_ids or set()
    due_ids = due_ids or set()
    ranked = []
    for problem in problems:
        problem_id = str(problem["id"])
        if problem_id in solved_ids and problem_id not in due_ids:
            continue
        topic = problem.get("topic", "arrays")
        current = float(mastery.get(topic, 0.35))
        difficulty = DIFFICULTY_VALUE.get(problem.get("difficulty", "Easy"), 0.25)
        target_success = max(0.05, min(0.95, 1 - abs(current - difficulty) * 1.35))
        zpd = 1 - abs(target_success - 0.675) / 0.675
        weak_topic = 1 - current
        due_bonus = 0.35 if problem_id in due_ids else 0.0
        popularity = float(problem.get("popularity_score", 0.5))
        score = 0.42 * zpd + 0.28 * weak_topic + 0.2 * due_bonus + 0.1 * popularity
        ranked.append(
            {
                **problem,
                "score": round(score, 4),
                "predicted_success": round(target_success, 3),
                "reason": "Due for spaced review" if problem_id in due_ids else f"Build momentum in {topic.replace('-', ' ').title()}",
                "ranked_at": datetime.now(UTC).isoformat(),
            }
        )
    return sorted(ranked, key=lambda item: item["score"], reverse=True)[:limit]
